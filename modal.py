import sqlite3


def FetchDailyTime(Marticule, Date):
    connection = sqlite3.connect('calenderApp.db', check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute(
        """SELECT duree FROM heures WHERE matricule ='{Marticule}' AND date_publication = '{Date}'; 
        """.format(Marticule=Marticule, Date=Date)
    )
    Time = None
    result = cursor.fetchone()
    if (result is None):
        Time = None
    else:
        Time = result[0]
        print(result[0])
    connection.commit()
    cursor.close()
    connection.close()
    return Time


def InsertTime(Marticule, Date, Time):
    connection = sqlite3.connect('calenderApp.db', check_same_thread=False)
    cursor = connection.cursor()

    cursor.execute(
        """INSERT INTO heures(matricule,date_publication,duree) VALUES('{Marticule}','{Date}','{Time}'); 
      """.format(Marticule=Marticule, Date=Date, Time=Time)
    )
    connection.commit()
    cursor.close()
    connection.close()
    return Time


def UpdateTime(Marticule, Date, Time):
    connection = sqlite3.connect('calenderApp.db', check_same_thread=False)
    cursor = connection.cursor()

    cursor.execute(
        """UPDATE heures SET duree='{Time}' WHERE matricule = '{Marticule}' AND date_publication = '{Date}'; 
        """.format(Time=Time, Marticule=Marticule, Date=Date)
    )
    connection.commit()
    cursor.close()
    connection.close()
    return True


def DeleteTime(Marticule, Date):
    connection = sqlite3.connect('calenderApp.db', check_same_thread=False)
    cursor = connection.cursor()

    cursor.execute(
        """DELETE FROM heures WHERE matricule = '{Marticule}' AND date_publication = '{Date}'; 
        """.format(Marticule=Marticule, Date=Date)
    )
    connection.commit()
    cursor.close()
    connection.close()
    return True


def FetchAllDataFromMonth(Marticule, Month):
    connection = sqlite3.connect('calenderApp.db', check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute(
        """SELECT duree,date_publication,matricule FROM heures WHERE matricule ='{Marticule}' AND (date_publication LIKE '%-{Month}-%' OR date_publication LIKE '%-0{Month}-%') Order By date_publication ASC; 
        """.format(Marticule=Marticule, Month=Month)
    )
    MarticuleData = []
    result = cursor.fetchall()
    if (result is None):
        MarticuleData = None
    else:
        for data in result:
            MarticuleData.append(data)

    connection.commit()
    cursor.close()
    connection.close()
    return MarticuleData


def fetchAllMonths(marticule):
    connection = sqlite3.connect('calenderApp.db', check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute(

        """SELECT date_publication FROM heures WHERE matricule ='{Marticule}'; 
        """.format(Marticule=marticule)
    )
    Date = []
    result = cursor.fetchall()
    if (result is None):
        Date = None
    else:
        for data in result:
            Date.append(data)
    connection.commit()
    cursor.close()
    connection.close()
    return Date
