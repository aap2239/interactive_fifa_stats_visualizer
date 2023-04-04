"""
Columbia's COMS W4111.001 Introduction to Databases
Example Webserver
To run locally:
    python server.py
Go to http://localhost:8111 in your browser.
A debugger such as "pdb" may be helpful for debugging.
Read about it online.
"""
import os

from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
app = Flask(__name__, template_folder=tmpl_dir)

DATABASE_USERNAME = "aap2239"
DATABASE_PASSWRD = "3205"
DATABASE_HOST = "34.28.53.86"  # change to 34.28.53.86 if you used database 2 for part 2
DATABASEURI = (
    f"postgresql://{DATABASE_USERNAME}:{DATABASE_PASSWRD}@{DATABASE_HOST}/project1"
)

engine = create_engine(DATABASEURI)


@app.before_request
def before_request():
    """
    This function is run at the beginning of every web request
    (every time you enter an address in the web browser).
    We use it to setup a database connection that can be used throughout the request.

    The variable g is globally accessible.
    """
    try:
        g.conn = engine.connect()
    except:
        print("uh oh, problem connecting to database")
        import traceback

        traceback.print_exc()
        g.conn = None


@app.teardown_request
def teardown_request(exception):
    """
    At the end of the web request, this makes sure to close the database connection.
    If you don't, the database could run out of memory!
    """
    try:
        g.conn.close()
    except Exception as e:
        pass


@app.route("/")
def index():
    """
    request is a special object that Flask provides to access web request information:

    request.method:   "GET" or "POST"
    request.form:     if the browser submitted a form, this contains the data in the form
    request.args:     dictionary of URL arguments, e.g., {a:1, b:2} for http://localhost?a=1&b=2

    See its API: https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data
    """

    # DEBUG: this is debugging code to see what request looks like
    print(request.args)
    return render_template("index.html")


@app.route("/countries")
def countries():
    try:
        select_query = """SELECT 
  							Country_ID, 
							Country_Name, 
							Country_Code, 
							Federation_Name, 
							Region_Name, 
							Confederation_Name, 
							Country_Wiki,
                            Confederation_Wiki
						FROM 
							Countries c1, 
							Confederations c2 
						WHERE 
							c1.Confederation_ID = c2.Confederation_ID;"""
        cursor = g.conn.execute(text(select_query))
        countries = []
        for result in cursor:
            countries_dict = {
                "Country_ID": result[0],
                "Country_Name": result[1],
                "Country_Code": result[2],
                "Federation_Name": result[3],
                "Region_Name": result[4],
                "Confederation_Name": result[5],
                "Country_Wiki": result[6],
                "Confederation_Wiki": result[7],
            }
            countries.append(countries_dict)
        cursor.close()
        context = dict(countries=countries)
        return render_template("countries.html", **context)
    except Exception as e:
        print(e)
        return render_template("error.html")


@app.route("/players")
def players():
    try:
        select_query = """SELECT 
  							Player_ID, 
							Player_Given_Name, 
							Player_Family_Name, 
							Player_Wiki, 
							Tournaments_Played 
						FROM 
							Players"""
        cursor = g.conn.execute(text(select_query))
        players = []
        for result in cursor:
            players_dict = {
                "player_id": result[0],
                "player_given_name": result[1],
                "player_family_name": result[2],
                "player_wiki": result[3],
                "Tournaments_Played": result[4],
            }
            players.append(players_dict)
        cursor.close()
        context = dict(players=players)
        return render_template("players.html", **context)
    except Exception as e:
        print(e)
        return render_template("error.html")


@app.route("/awards")
def awards():
    try:
        select_query = """SELECT 
  							Award_ID, 
							Award_Name, 
							Award_Description, 
							Year_Introduced
						FROM 
							Awards"""
        cursor = g.conn.execute(text(select_query))
        awards = []
        for result in cursor:
            awards_dict = {
                "award_id": result[0],
                "award_name": result[1],
                "award_description": result[2],
                "year_introduced": result[3],
            }
            awards.append(awards_dict)
        cursor.close()
        context = dict(awards=awards)
        return render_template("awards.html", **context)
    except Exception as e:
        print(e)
        return render_template("error.html")


@app.route("/managers")
def managers():
    try:
        select_query = """SELECT 
  							Manager_ID, 
							Manager_Given_Name, 
							Manager_Family_Name, 
							Manager_Wiki
						FROM 
							Managers"""
        cursor = g.conn.execute(text(select_query))
        managers = []
        for result in cursor:
            managers_dict = {
                "manager_id": result[0],
                "manager_given_name": result[1],
                "manager_family_name": result[2],
                "manager_wiki": result[3],
            }
            managers.append(managers_dict)
        cursor.close()
        context = dict(managers=managers)
        return render_template("managers.html", **context)
    except Exception as e:
        print(e)
        return render_template("error.html")
    
@app.route("/squads")
def squads():
    try:
        select_query = """SELECT 
  							Squad_ID, 
							Country_Name, 
							Tournament_Name, 
							Manager_Given_Name,
                            Manager_Family_Name
						FROM 
							Squads s1,
                            Managers m1, 
                            Tournaments t1, 
                            Countries c1
                        WHERE
                            s1.manager_id = m1.manager_id AND
                            s1.tournament_id = t1.tournament_id AND
                            s1.country_id = c1.country_id;"""
        cursor = g.conn.execute(text(select_query))
        squads = []
        for result in cursor:
            squads_dict = {
                "squad_id": result[0],
                "country_name": result[1],
                "tournament_name": result[2],
                "manager_given_name": result[3],
                "manager_family_name": result[4],
            }
            squads.append(squads_dict)
        cursor.close()
        context = dict(squads=squads)
        return render_template("squads.html", **context)
    except Exception as e:
        print(e)
        return render_template("error.html")


@app.route("/confederations")
def confederations():
    try:
        select_query = """SELECT 
  							Confederation_ID, 
							Confederation_Name, 
							Confederation_Code, 
							Confederation_Wiki
						FROM 
							Confederations"""
        cursor = g.conn.execute(text(select_query))
        confederations = []
        for result in cursor:
            confederations_dict = {
                "confederation_id": result[0],
                "confederation_name": result[1],
                "confederation_code": result[2],
                "confederation_wiki": result[3],
            }
            confederations.append(confederations_dict)
        cursor.close()
        context = dict(confederations=confederations)
        return render_template("confederations.html", **context)
    except Exception as e:
        print(e)
        return render_template("error.html")


@app.route("/add_players", methods=["POST", "GET"])
def add_players():
    if request.method == "POST":
        cursor = g.conn.execute(
            text("SELECT MAX(SUBSTR(Player_ID, 3)) AS Max_Player_ID FROM Players;")
        )
        result = cursor.fetchall()[-1][-1]
        cursor.close()
        print(result, " - Result")
        temp = int(result)
        temp += 1
        player_id = "P-" + str(temp)
        player_given = request.form["player_given_name"]
        player_family = request.form["player_family_name"]
        player_wiki = request.form["player_wiki"]
        num_tournaments = request.form["tournaments_played"]

        query = f"INSERT INTO PLAYERS VALUES ('{player_id}', '{player_given}','{player_family}', '{player_wiki}', '{num_tournaments}')"
        g.conn.execute(text(query))
        g.conn.commit()
        try:
            select_query = """SELECT 
                                Player_ID, 
                                Player_Given_Name, 
                                Player_Family_Name, 
                                Player_Wiki, 
                                Tournaments_Played 
                            FROM 
                                Players"""
            cursor = g.conn.execute(text(select_query))
            players = []
            for result in cursor:
                players_dict = {
                    "player_id": result[0],
                    "player_given_name": result[1],
                    "player_family_name": result[2],
                    "player_wiki": result[3],
                    "Tournaments_Played": result[4],
                }
                players.append(players_dict)
            cursor.close()
            context = dict(players=players)
            return render_template("players.html", **context)
        except Exception as e:
            print(e)
            return render_template("error.html")

    return render_template("add_players.html")


@app.route("/login")
def login():
    abort(401)
    this_is_never_executed()


if __name__ == "__main__":
    import click

    @click.command()
    @click.option("--debug", is_flag=True)
    @click.option("--threaded", is_flag=True)
    @click.argument("HOST", default="0.0.0.0")
    @click.argument("PORT", default=8111, type=int)
    def run(debug, threaded, host, port):
        """
        This function handles command line parameters.
        Run the server using:

                python server.py

        Show the help text using:

                python server.py --help

        """

        HOST, PORT = host, port
        print("running on %s:%d" % (HOST, PORT))
        app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)


run()
