from flask import  *
import sqlite3

app = Flask(__name__)
app.secret_key = "cng445bestcourse"


#home page
@app.route("/")
@app.route("/home/")
def home():
    conn = sqlite3.connect("advertisements.db")
    c = conn.cursor()
    c.execute("SELECT cid,cname FROM CATEGORY")
    availableCategories = c.fetchall()
    conn.close()
    if "user" in session:
        return render_template("home.html", username=session["user"], availableCategory=availableCategories)
    else:
        return render_template("home.html", availableCategory=availableCategories)

#end point that direct to login page
@app.route("/login/")
def loginpage():
    return render_template("login.html")

#here, when user clicks submit button on the login form, this end point is triggered
#if there is no username in the database that user tries to login, they will see an error message
@app.post("/dologin/")
def dologin():
    username = request.form["username"]
    password = request.form["password"]
    conn = sqlite3.connect("advertisements.db")
    c = conn.cursor()
    c.execute("SELECT * FROM USER WHERE username=? AND password=?",(username, password))
    row = c.fetchone()
    if row != None:
        session["user"] = username
        return redirect(url_for("home"))
    else:
        return render_template("login.html", error=True)


#this endpoint directs user to register.html
@app.route("/register/")
def registerpage():
    return render_template("register.html")


#here, this end point is triggered when user fills the registration form then submits it
#in this form, we are checking specific error conditions and based on these conditions, the registeration is successful or not
@app.post("/doregister/")
def doregister():
    username = request.form["username"]
    conn = sqlite3.connect("advertisements.db")
    c = conn.cursor()
    c.execute("SELECT * FROM USER WHERE username=?", (username, ))
    row = c.fetchone()
    conn.close()
    if row != None:
        return render_template("register.html", usernameError=True)
    else:
        password = request.form["password"]
        fullname = request.form["fullname"]
        email = request.form["email"]
        telno = request.form["telno"]
        newUser = (username, password, fullname, email, telno)

        conn = sqlite3.connect("advertisements.db")
        c = conn.cursor()
        c.execute("INSERT INTO USER VALUES(?,?,?,?,?)", newUser)
        conn.commit()
        conn.close()
        return render_template("successfulregister.html")


#this is the part when user enters a username, if the text they entered is already in the database, they are warned with a message
#they this username is already taken, so that they cant take it
@app.get("/gethint")
def gethint():
    suggestions = []
    conn = sqlite3.connect("advertisements.db")
    c = conn.cursor()
    c.execute("SELECT username FROM USER")
    records = c.fetchall()
    names = []
    for name in records:
        names.append(name[0])


    q = request.args.get("q", None)
    if q != None:
        for name in names:
            if q.lower() == name.lower():
                suggestions.append(name)
    return ", ".join(suggestions)


#directs user to his/her profile
#in this part, they can edit their informations

@app.route("/myprofile/")
def myprofile():
    conn = sqlite3.connect("advertisements.db")
    c = conn.cursor()
    c.execute("SELECT * FROM USER WHERE username=?",(session["user"], ))
    records = c.fetchone()

    return render_template("myprofile.html", userdata=records)


#this is the ndpoint when the user tries to edit their informations
#if they are trying to edit their username as an existing user's username, they will get an error
#otherwise, their information will be updated succesfully
@app.post("/editprofile/")
def editprofile():
    newusername = request.form["username"]
    newpassword = request.form["password"]
    newfullname = request.form["fullname"]
    newemail = request.form["email"]
    newtelno = request.form["telno"]
    userdata = (newusername, newpassword, newfullname, newemail, newtelno)

    conn = sqlite3.connect("advertisements.db")
    c = conn.cursor()
    c.execute("SELECT username FROM USER")
    records = c.fetchall()

    for record in records:
        # this means that user tries to edit an existing username but not her/his current username
        if (record[0] == newusername) and (record[0] != session["user"]):
            return render_template("myprofile.html", userdata=userdata, error="usernameerror")

    #if we come this line, this means we have no error and can update the user details

    editUser = userdata + (session["user"], )

    c.execute("UPDATE USER SET username=?, password=?, fullname=?, email=?, telno=? WHERE username=?", editUser)
    c.execute("UPDATE ADVERTISEMENT SET username=? WHERE username=?", (newusername, session["user"]))
    conn.commit()



    conn.close()
    # if user chanced his/her username, set the new username into session
    session["user"] = newusername
    return render_template("myprofile.html", userdata=userdata, error="noerror")


#this is the part where user can see their advertisements, active/deactive them, and also can add new advertisement
@app.route("/myadvertisements/")
def myadvertisements():
    conn = sqlite3.connect("advertisements.db")
    c = conn.cursor()
    c.execute("SELECT cname FROM CATEGORY")
    availableCategories = c.fetchall()

    c.execute("SELECT a.title, a.description, c.cname, a.isactive, a.aid FROM ADVERTISEMENT a, CATEGORY c WHERE "
              "c.cid=a.cid  AND a.username=?", (session["user"], ))
    previouslyAdvertisements = c.fetchall()
    conn.close()
    return render_template("myadvertisements.html", availableCategory=availableCategories, previouslyAdvertisements=previouslyAdvertisements)


#this is the enddpoint that is triggered when user tried to add a new advertisement
@app.post("/addadvertisement/")
def addadvertisement():
    title = request.form["title"]
    description = request.form["description"]
    categoryName = request.form["categories"]

    conn = sqlite3.connect("advertisements.db")
    c = conn.cursor()
    c.execute("SELECT cid FROM CATEGORY WHERE cname=?",(categoryName, ))
    row = c.fetchone()
    categoryID = row[0]

    newAdvertisement = (title,description, 1, categoryID, session["user"])

    c.execute("INSERT INTO ADVERTISEMENT(title, description, isactive, cid, username) VALUES(?,?,?,?,?)", newAdvertisement)
    conn.commit()
    conn.close()
    return render_template("successfuladvertisement.html")


#this is the part where user tries to activate a deactivated advertisement
@app.route("/activateadvertisement/<aid>/")
def activateadvertisement(aid):
    conn = sqlite3.connect("advertisements.db")
    c = conn.cursor()
    c.execute("UPDATE ADVERTISEMENT SET isactive=? WHERE aid=?", (1, aid))
    conn.commit()
    conn.close()
    activationStatus = "active"
    return render_template("successfulisactive.html", activationStatus=activationStatus)

#this is the part where user tries to deactivate an activated advertisement
@app.route("/deactivateadvertisement/<aid>/")
def deactivateadvertisement(aid):
    conn = sqlite3.connect("advertisements.db")
    c = conn.cursor()
    c.execute("UPDATE ADVERTISEMENT SET isactive=? WHERE aid=?", (0, aid))
    conn.commit()
    conn.close()
    activationStatus = "deactive"
    return render_template("successfulisactive.html", activationStatus=activationStatus)

#this is the part where user search for active advertisements
@app.get("/searchadvertisement/")
def searchadvertisement():
    searchedKeyword = request.args.get("searchbox", None)
    selectedCategory = request.args.get("categories", None)

    conn = sqlite3.connect("advertisements.db")
    c = conn.cursor()

    # to make it all category, remove a.cid=?
    if selectedCategory == "All Categories":
        c.execute(f"SELECT a.title, a.description, u.fullname, c.cname, a.aid FROM ADVERTISEMENT a, USER u, CATEGORY c WHERE "
                  f"a.username=u.username AND a.cid=c.cid AND a.isactive=? AND "
                  f"("
                  f"a.title LIKE '%{searchedKeyword}%' OR "
                  f"a.description LIKE '%{searchedKeyword}%' OR "
                  f"u.fullname LIKE '%{searchedKeyword}%')  ORDER BY c.cname ", (1, ))
        records = c.fetchall()

        availableCategories = []
        for line in records:
            if line[3] not in availableCategories:
                availableCategories.append(line[3])



        c.execute("SELECT cid,cname FROM CATEGORY")
        categories = c.fetchall()
        allcategories = []
        for category in categories:
            allcategories.append(category[1])

        #first of all, this part is little complicated, sorry for that. The idea for displaying all categories with unique labes
        #and no advertisement for categories that has no advertisement is as follows:

        #we took the all categories, then we took the available categories in the database
        #after, we took the difference of these categories to achive the categories that has no advertisement

        #later, we categorized the data which has same category. For example, if we have 3 advertisements in a fetched record
        #we try to achive a nested list like this
        #groupedList = [
        #               [(..."clothes"),(....,"clothes")],
        #               [(...,"food")]
        #           ]
        #in this way, we can create our new table based on the categories
        #for example, when we say -> for group in grouplist, we can get the advertisements which has same category
        #then we sent all of these informations into our home.html

        notAvailableCategories = {}
        notAvailableCategories = set(allcategories) - set(availableCategories)
        notAvailableCategories = list(notAvailableCategories)


        groupedList = []
        startIndex = 0

        currentCategory = records[0][3]
        for i in range(1, len(records)):
            if records[i][3] != currentCategory:
                groupedList.append(records[startIndex:i])
                startIndex = i

            currentCategory = records[i][3]

        groupedList.append(records[startIndex:])

        conn.close()
        if "user" in session:
            return render_template("home.html",username=session["user"], availableCategory=categories, advertisements=records,
                                   categoryname="All Categories", groupedList=groupedList, allcategories=allcategories,
                                   notAvailableCategories=notAvailableCategories, )
        else:
            return render_template("home.html",  availableCategory=categories, advertisements=records,
                                   categoryname="All Categories", groupedList=groupedList, allcategories=allcategories,
                                   notAvailableCategories=notAvailableCategories)

    # this is the part if the category selected is not all categories
    #the difference from all category is that we are sent the selectedCategories ID into query so that we can get advertisements that has a specific category
    else:

        c.execute("SELECT cid,cname FROM CATEGORY")
        categories = c.fetchall()

        c.execute(f"SELECT a.title, a.description, u.fullname, a.aid FROM ADVERTISEMENT a, USER u, CATEGORY c WHERE "
                  f"a.username=u.username AND a.cid=c.cid AND a.isactive=? AND "
                  f"a.cid=? AND ("
                  f"a.title LIKE '%{searchedKeyword}%' OR "
                  f"a.description LIKE '%{searchedKeyword}%' OR "
                  f"u.fullname LIKE '%{searchedKeyword}%')", (1, selectedCategory))
        records = c.fetchall()

        conn.close()
        if "user" in session:
            return render_template("home.html",username=session["user"],availableCategory=categories, advertisements=records, categoryname=None)
        else:
            return render_template("home.html", availableCategory=categories, advertisements=records, categoryname=None)


#this is the part where user wants to see more details about a specific advertisement
@app.route("/moreinfoadvertisement/<aid>")
def moreinfoadvertisement(aid):
    conn = sqlite3.connect("advertisements.db")
    c = conn.cursor()
    c.execute("SELECT a.title, a.description, c.cname, u.fullname, u.email, u.telno FROM ADVERTISEMENT a, USER u, CATEGORY c WHERE "
              "a.username=u.username AND a.cid=c.cid AND a.aid=?", (aid, ))
    records = c.fetchall()
    return render_template("moreinfoadvertisement.html", moredetails=records)


#simple logout process
@app.route("/logout/")
def logout():
    session.pop("user", None)
    return redirect(url_for("home"))






if __name__ == "__main__":
    app.run()















