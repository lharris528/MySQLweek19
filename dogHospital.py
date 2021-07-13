import pymysql
from flask import Flask, request, render_template

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/add", methods=["GET"])
def addDogtor():
    return render_template("add.html")


@app.route("/addSomething", methods=["POST"])
def addSomething():
    db = pymysql.connect(
        host="freetrainer.cryiqqx3x1ub.us-west-2.rds.amazonaws.com",
        user="leaf",
        password="changeme"
    )
    cursor = db.cursor()
# Variable to be assigned based on user action
    sqlQuery = ""

# Add a Dogtor
    if request.form.get('dogtorFirstName'):
        firstName = request.form['dogtorFirstName']
        lastName = request.form['last']
        sqlQuery = f"""INSERT INTO leaf.dogtors (firstName, lastName, fullName) VALUES
                  ("{firstName}", "{lastName}", "{firstName} {lastName}")"""


# Add a Doge
    if request.form.get('first'):
        firstName = request.form['first']
        lastName = request.form['last']
        breed = request.form['breed']
        weight = request.form['weight']
        age = request.form['age']
        color = request.form['color']
        dogtorID = request.form['dogtorID']
        maladyID = request.form['maladyID']
        sqlQuery = f"""INSERT INTO leaf.dogs (firstName, lastName, fullName, breed, weight, age, color, doctorID, maladyID) VALUES
                  ("{firstName}", "{lastName}", "{firstName} {lastName}", "{breed}",
                  "{weight}", "{age}", "{color}", "{dogtorID}", "{maladyID}")"""

# Add a Malady
    if request.form.get('malady'):
        malady = request.form['malady']
        sqlQuery = f"""INSERT INTO leaf.maladies (malady) VALUES
                  ("{malady}")"""

    cursor.execute(sqlQuery)
    db.commit()
    db.close()
    return render_template("home.html")


@app.route("/delete", methods=["GET"])
def delete():
    return render_template("delete.html")


@app.route("/deleteSomething", methods=['POST'])
def deleteSomething():
    db = pymysql.connect(
        host="freetrainer.cryiqqx3x1ub.us-west-2.rds.amazonaws.com",
        user="leaf",
        password="changeme"
    )
    cursor = db.cursor()
# Variables to be assigned based on user action
    deleteID = ""
    deleteFrom = ""

# Delete a Dogtor
    if request.form.get('deleteDogtor'):
        deleteID = request.form['deleteDogtor']
        deleteFrom = "leaf.dogtors"

# Delete a Doge
    if request.form.get('deleteDoge'):
        deleteID = request.form['deleteDoge']
        deleteFrom = "leaf.dogs"

# Delete a Malady
    if request.form.get('deleteMalady'):
        deleteID = request.form['deleteMalady']
        deleteFrom = "leaf.maladies"
    sqlQuery = f"""DELETE FROM {deleteFrom}
               WHERE id = '{deleteID}'"""
    cursor.execute(sqlQuery)
    db.commit()
    db.close()
    return render_template("home.html")


@app.route("/update", methods=["GET"])
def update():
    return render_template("update.html")


@app.route("/updateSomething", methods=["POST"])
def updateSomething():
    db = pymysql.connect(
        host="freetrainer.cryiqqx3x1ub.us-west-2.rds.amazonaws.com",
        user="leaf",
        password="changeme"
    )
    cursor = db.cursor()
# Variable to be assigned based on user action
    sqlQuery = ""

# Updating a Dogtor
    if request.form.get('dogtorID'):
        dogtorID = request.form['dogtorID']
        dogtorID = int(dogtorID)
        first = request.form['first']
        last = request.form['last']
        sqlQuery = f"""UPDATE leaf.dogtors
                  SET lastName = '{last}',
                  firstName = '{first}'
                  WHERE id = {dogtorID}"""

# Updating a Doge
    if request.form.get('dogeID'):
        dogeID = request.form['dogeID']
        firstName = request.form['first']
        lastName = request.form['last']
        breed = request.form['breed']
        weight = request.form['weight']
        age = request.form['age']
        color = request.form['color']
        dogtorID = request.form['dogtorID']
        DMID = request.form['dogeMaladyID']
        sqlQuery = f"""UPDATE leaf.dogs
                  SET firstName = '{firstName}',
                      lastName = '{lastName}',
                      fullName = '{firstName} {lastName}',
                      breed = '{breed}',
                      weight = '{weight}',
                      age = '{age}',
                      color = '{color}',
                      doctorID = '{dogtorID}',
                      maladyID = '{DMID}'
                  WHERE id = {dogeID}"""

# Updating a Malady
    if request.form.get('maladyID'):
        maladyID = request.form['maladyID']
        maladyID = int(maladyID)
        malady = request.form['maladyUpdate']
        sqlQuery = f"""UPDATE leaf.maladies
                  SET malady = '{malady}'
                  WHERE id = {maladyID}"""

    cursor.execute(sqlQuery)
    db.commit()
    db.close()
    return render_template("/update.html")


@app.route("/search", methods=["POST"])
def search():
    db = pymysql.connect(
        host="freetrainer.cryiqqx3x1ub.us-west-2.rds.amazonaws.com",
        user="leaf",
        password="changeme"
    )
# Variables to be assigned based on user action
    sqlQuery = ""

# Searching by doge name
    if request.form.get('dogName'):
        dogName = request.form['dogName']
        cursor = db.cursor()
        sqlQuery = f"""SELECT dogs.id AS ID, dogs.fullName AS Doge, dogs.breed AS Breed,
        maladies.malady AS Malady, dogtors.fullName AS Dogtor
        FROM leaf.dogs
        JOIN leaf.dogtors ON dogtors.id = dogs.doctorID
        JOIN leaf.maladies ON maladies.id = dogs.maladyID
        WHERE dogs.fullName LIKE '{dogName}%'"""

# Searching by Breed
    if request.form.get('breed'):
        dogBreed = request.form['breed']
        cursor = db.cursor()
        sqlQuery = f"""SELECT dogs.breed AS Breed, dogs.fullName AS Doge, maladies.malady AS Malady, dogtors.fullName AS Dogtor
                  FROM leaf.dogs
                  JOIN leaf.dogtors ON dogtors.id = dogs.doctorID
                  JOIN leaf.maladies ON maladies.id = dogs.maladyID
                  WHERE dogs.breed LIKE '{dogBreed}%'"""

# Searching by Dogtor
    if request.form.get('dogtor'):
        dogtor = request.form['dogtor']
        cursor = db.cursor()
        sqlQuery = f"""SELECT dogtors.ID AS ID, dogtors.fullName AS Dogtor, dogs.fullName AS Doge,
                  dogs.breed AS Breed, maladies.malady AS Malady
                  FROM leaf.dogs
                  JOIN leaf.dogtors ON dogtors.id = dogs.doctorID
                  JOIN leaf.maladies ON maladies.id = dogs.maladyID
                  WHERE dogtors.fullName LIKE '{dogtor}%'"""

# Searching by Malady
    if request.form.get('malady'):
        malady = request.form['malady']
        cursor = db.cursor()
        sqlQuery = f"""SELECT maladies.id AS ID, maladies.malady AS Malady, dogs.fullName AS Doge,
                  dogs.breed AS Breed, dogtors.fullName AS Dogtor
                  FROM leaf.dogs
                  JOIN leaf.dogtors ON dogtors.id = dogs.doctorID
                  JOIN leaf.maladies ON maladies.id = dogs.maladyID
                  WHERE maladies.malady LIKE '{malady}%'"""

    cursor.execute(sqlQuery)
    searchResults = cursor.fetchall()

    return render_template("search.html", searchResults=searchResults)

if __name__ == '__main__':
    app.run(debug=True)
