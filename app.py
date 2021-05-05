from flask import Flask, render_template, redirect, url_for, request
import modal
from datetime import timedelta
from datetime import datetime


TodaysDateGlobal = ""
PreviousDateGlobal = ""
NextDateGlobal = ""
global count
count = "1"
nextShow = True
PreviousShow = True


def MonthsSet(argument):
    switcher = {
        1: "January",
        2: "February",
        3: "March",
        4: "April",
        5: "May",
        6: "June",
        7: "July",
        8: "August",
        9: "September",
        10: "October",
        11: "November",
        12: "December"
    }
    return switcher.get(argument, "Invalid month")


app = Flask(__name__)

# homepage for validating user code


@app.route('/process', methods=['POST', "GET"])
def processOverview():
    global nextShow
    global PreviousShow
    if (request.method == "POST"):
        if (request.form["action"] == "overviewOfMonth"):
            marticule = request.form['marticule']
            date = request.form['dateOfDay']
            date = datetime.strptime(
                date, '%d-%m-%Y').date()
            month = date.month
            return redirect(url_for("overviewMonth", marticule=marticule, month=month))

        elif (request.form["action"] == "yearly"):
            marticule = request.form["marticule"]
            return redirect(url_for("overview", marticule=marticule))

        elif (request.form['action'] == "MonthSelect"):
            marticule = request.form["marticule"]
            month = request.form["month"]
            return redirect(url_for("overviewMonth", marticule=marticule, month=month))

        elif (request.form["action"] == "nextMonth"):
            marticule = request.form['marticule']
            Month = request.form['Month']
            print("This is Month: ", Month)
            Month = str(Month)
            if (int(Month)+1 <= 12):
                Month = int(Month) + 1
                Month = str(Month)

                return redirect(url_for("overviewMonth", marticule=marticule, month=Month))
            else:
                Month = str(Month)
                nextShow = False
                return redirect(url_for("overviewMonth", marticule=marticule, month=Month))
        elif (request.form["action"] == "previousMonth"):
            marticule = request.form['marticule']
            Month = request.form['Month']
            Month = str(Month)
            if (int(Month)-1 > 0):
                Month = int(Month) - 1
                Month = str(Month)
                if (int(Month)-1 == 1):
                    PreviousShow = False
                else:
                    PreviousShow = True
                return redirect(url_for("overviewMonth", marticule=marticule, month=Month))
            else:
                Month = str(Month)
                PreviousShow = False
                return redirect(url_for("overviewMonth", marticule=marticule, month=Month))
    else:
        return redirect(url_for("index"))


@app.route('/', methods=['GET', 'POST'])
def index():
    global count
    if request.method == 'POST':
        if request.form['action'] == "sendUserCode":
            marticule = request.form['marticule']
            dateToday = datetime.today()
            dateToday = dateToday.strftime("%d-%m-%Y")
            TodaysDateGlobal = dateToday
            count = "1"
            return redirect(url_for('date_du_jour', marticule=marticule, date_du_jour=dateToday))
        else:
            return render_template('index.html')
    else:
        return render_template('index.html')

# marticule date of journey


@app.route('/<marticule>/<date_du_jour>', methods=['GET', 'POST'])
def date_du_jour(marticule, date_du_jour):
    global count

    if request.method == 'POST':
        if (request.form['action'] == "previousDate"):
            dateFixed = datetime.today()
            dateFixed = dateFixed.strftime('%d-%m-%Y')

            dateToday = request.form['dateOfDay']
            marticule = request.form['marticule']

            dateToday = datetime.strptime(
                dateToday, '%d-%m-%Y').date()-timedelta(days=1)
            dateToday = dateToday.strftime('%d-%m-%Y')
            if (dateToday != dateFixed):
                check = True
                Time = modal.FetchDailyTime(marticule, dateToday)
                if (Time is None):
                    check = False
                    count = "2"
                    return redirect(url_for("date_du_jour", marticule=marticule, date_du_jour=dateToday))
                else:
                    count = "2"
                    return redirect(url_for("date_du_jour", marticule=marticule, date_du_jour=dateToday))
            elif (dateToday == dateFixed):
                count = "1"
                return redirect(url_for("date_du_jour", marticule=marticule, date_du_jour=dateFixed))
            else:
                count = "2"
                return redirect(url_for("date_du_jour", marticule=marticule, date_du_jour=dateToday))

        if (request.form['action'] == "nextDate"):
            dateFixed = datetime.today()
            dateFixed = dateFixed.strftime('%d-%m-%Y')

            dateToday = request.form['dateOfDay']
            marticule = request.form['marticule']

            dateToday = datetime.strptime(
                dateToday, '%d-%m-%Y').date()+timedelta(days=1)
            dateToday = dateToday.strftime('%d-%m-%Y')
            if (dateToday != dateFixed):
                check = True
                Time = modal.FetchDailyTime(marticule, dateToday)
                if (Time is None):
                    check = False

                    return redirect(url_for("date_du_jour", marticule=marticule, date_du_jour=dateToday))
                else:

                    return redirect(url_for("date_du_jour", marticule=marticule, date_du_jour=dateToday))
            elif (dateToday == dateFixed):
                count = "1"
                return redirect(url_for("date_du_jour", marticule=marticule, date_du_jour=dateFixed))
            else:
                count = "2"
                return redirect(url_for("date_du_jour", marticule=marticule, date_du_jour=dateToday))
        elif (request.form['action'] == "addTodaysTime"):
            inputTime = request.form['timeOfDay']
            dateToday = request.form['dateOfDay']
            marticule = request.form['marticule']
            #
            # Here we will add addingTime to current date query
            #
            #
            TodaysDateGlobal = dateToday
            modal.InsertTime(marticule, dateToday, inputTime)
            return redirect(url_for("date_du_jour", marticule=marticule, date_du_jour=dateToday))
        elif (request.form['action'] == "update"):
            marticule = request.form['marticule']
            date = request.form['dateOfDay']
            time = request.form['timeOfDay']

            #
            # Here we will update time to date mentioned to the query
            #
            #
            check = modal.UpdateTime(marticule, date, time)
            if (check == True):

                return redirect(url_for("date_du_jour", marticule=marticule, date_du_jour=date))
            else:

                error = "Not Updated"
                return redirect(url_for("date_du_jour", marticule=marticule, date_du_jour=date))

                # Error Message Here
            # update that time of the day from database under that employee
        elif (request.form['action'] == "delete"):

            marticule = request.form['marticule']
            date = request.form['dateOfDay']

            #
            # Here we will delete time to date mentioned to the query
            #
            #
            check = modal.DeleteTime(marticule, date)
            if (check == True):
                dateFixed = datetime.today()
                dateFixed = dateFixed.strftime('%d-%m-%Y')
                date = datetime.strptime(
                    date, '%d-%m-%Y').date()
                date = date.strftime('%d-%m-%Y')
                if (date == dateFixed):
                    count = "1"
                    return redirect(url_for("date_du_jour", marticule=marticule, date_du_jour=date))
                else:
                    return redirect(url_for("date_du_jour", marticule=marticule, date_du_jour=date))

            else:

                error = "Not Updated"
                return redirect(url_for("date_du_jour", marticule=marticule, date_du_jour=date))
            # delete that time of the day from database under that employee
    else:

        check = True
        Time = modal.FetchDailyTime(marticule, date_du_jour)
        if (Time is None):
            check = False
            if count == "1":
                count = "2"
                return render_template('marticule.html', Time=Time, check=check, count="1", Date=date_du_jour, marticule=marticule)
            else:
                count = "2"
        return render_template('marticule.html', Time=Time, check=check, count=count, Date=date_du_jour, marticule=marticule)
# marticule date of journey


@app.route('/<marticule>/overview/<month>')
def overviewMonth(marticule, month):

    #
    # Here we will display all the data from the month and time on the page from
    # query
    #

    marticuleData = []

    if (int(month) == 12):
        nextShow = False
    else:
        nextShow = True
    if (int(month) == 1):
        PreviousShow = False
    else:
        PreviousShow = True
    marticuleData = modal.FetchAllDataFromMonth(marticule, month)
    return render_template('overview.html', marticuleData=marticuleData, marticule=marticule, month=month, nextShow=nextShow, PreviousShow=PreviousShow)

# marticule


@app.route('/<marticule>')
def overview(marticule):

    months = []

    Date = modal.fetchAllMonths(marticule)
    for i in Date:
        DateVariable = datetime.strptime(i[0], '%d-%m-%Y').date()
        months.append(DateVariable.strftime('%m'))

    myset = set(months)
    months = list(myset)
    monthsName = []
    for x in months:
        monthsName.append([x, MonthsSet(int(x))])
    return render_template('marticule_date.html', marticule=marticule, monthsName=monthsName)


app.run(port=3000, debug=True)
