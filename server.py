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
from sqlalchemy import create_engine, text
from sqlalchemy.sql.expression import bindparam
from sqlalchemy.dialects.postgresql import ARRAY

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
                "Country_Details_URL": f"/country/{result[0]}",
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
        # Get the squad_ids from the form and split them by commas
        squad_ids = request.form["squad_ids"].split(',')
        if True:
            if True:
                cursor = g.conn.execute(
                    text("SELECT MAX(SUBSTR(Player_ID, 3)) AS Max_Player_ID FROM Players;")
                )
                result = cursor.fetchall()[-1][-1]
                cursor.close()
                temp = int(result)
                temp += 1
                player_id = "P-" + str(temp)
                player_given = request.form["player_given_name"]
                player_family = request.form["player_family_name"]
                player_wiki = request.form["player_wiki"]
                num_tournaments = request.form["tournaments_played"]
                if player_wiki == "":
                    query = f"INSERT INTO Players (player_id, player_given_name, player_family_name, tournaments_played) VALUES ('{player_id}', '{player_given}','{player_family}', '{num_tournaments}')"
                else:
                    query = f"INSERT INTO PLAYERS VALUES ('{player_id}', '{player_given}','{player_family}', '{player_wiki}', '{num_tournaments}')"
                g.conn.execute(text(query))

                # Update the Squads table to append the player_id to the player_ids array for each squad_id
                for squad_id in squad_ids:
                    update_squads_query = f"UPDATE Squads SET Player_IDs = array_append(Player_IDs, '{player_id}') WHERE Squad_ID = '{squad_id.strip()}'"
                    g.conn.execute(text(update_squads_query))

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

            else:
                # Handle case when one or more squad_ids don't exist in the Squads table
                error_message = "One or more squad_ids don't exist in the Squads table. Please provide valid squad_ids."
                return render_template("error.html", error_message=error_message)
        else:
            # Handle case when the tournament years for different squads are not different
            error_message = "The tournament years for different squads must be different. Please provide squads with different tournament years."
            return render_template("error.html", error_message=error_message)

    return render_template("add_players.html")


@app.route("/awards_won", methods=["POST", "GET"])
def awards_won():
    if request.method == "POST":
        award_name = request.form["award_name"]

        if len(award_name) > 0:
            select_query = f"""SELECT 
  							award_name, 
							player_given_name, 
							player_family_name, 
							tournament_name
						FROM 
							awards a1,
                            players p1,
                            tournaments t1,
                            has_won hw1
                        WHERE
                            hw1.award_id = a1.award_id AND
                            hw1.player_id = p1.player_id AND 
                            hw1.tournament_id = t1.tournament_id AND 
                            a1.award_name = \'{award_name}\'
                        ORDER BY 
                            tournament_name, award_name;"""
        else:
            select_query = f"""SELECT 
  							award_name, 
							player_given_name, 
							player_family_name, 
							tournament_name
						FROM 
							awards a1,
                            players p1,
                            tournaments t1,
                            has_won hw1
                        WHERE
                            hw1.award_id = a1.award_id AND
                            hw1.player_id = p1.player_id AND 
                            hw1.tournament_id = t1.tournament_id
                        ORDER BY 
                            tournament_name, award_name;"""
        try:

            cursor = g.conn.execute(text(select_query))
            awards_won = []
            for result in cursor:
                awards_won_dict = {
                    "award_name": result[0],
                    "player_given_name": result[1],
                    "player_family_name": result[2],
                    "tournament_name": result[3],
                }
                awards_won.append(awards_won_dict)
            cursor.close()
            context = dict(awards_won=awards_won)
            return render_template("awards_won.html", **context)
        except Exception as e:
            print(e)
            return render_template("error.html")

    try:
        select_query = """SELECT 
  							award_name, 
							player_given_name, 
							player_family_name, 
							tournament_name
						FROM 
							awards a1,
                            players p1,
                            tournaments t1,
                            has_won hw1
                        WHERE
                            hw1.award_id = a1.award_id AND
                            hw1.player_id = p1.player_id AND 
                            hw1.tournament_id = t1.tournament_id
                        ORDER BY 
                            tournament_name, award_name;"""
        cursor = g.conn.execute(text(select_query))
        awards_won = []
        for result in cursor:
            awards_won_dict = {
                "award_name": result[0],
                "player_given_name": result[1],
                "player_family_name": result[2],
                "tournament_name": result[3],
            }
            awards_won.append(awards_won_dict)
        cursor.close()
        context = dict(awards_won=awards_won)
        return render_template("awards_won.html", **context)
    except Exception as e:
        print(e)
        return render_template("error.html")
    
@app.route("/country/<country_id>")
def country_details(country_id):
    try:
        select_query = f"""SELECT 
                              Country_Name, 
                              countries_wiki_intro 
                            FROM 
                              Countries
                            WHERE
                              Country_ID = '{country_id}';"""
        cursor = g.conn.execute(text(select_query))
        result = cursor.fetchone()
        cursor.close()
        if result:
            country_name = result[0]
            wiki_intro = result[1]
            return render_template("country_details.html", country_name=country_name, wiki_intro=wiki_intro)
        else:
            return render_template("error.html")
    except Exception as e:
        print(e)
        return render_template("error.html")
    
@app.route("/squad_members", methods=["POST", "GET"])
def squad_members():
    if request.method == "POST":
        squad_id = request.form["squad_id"]
        select_query = f"""SELECT 
                                a1.squad_id, 
                                p1.player_given_name, 
                                p1.player_family_name, 
                                t1.tournament_name
                            FROM 
                                squads a1,
                                players p1,
                                tournaments t1
                            WHERE
                                a1.tournament_id = t1.tournament_id AND
                                a1.squad_id = \'{squad_id}\' AND
                                p1.player_id = ANY(a1.player_ids)"""

        try:
            cursor = g.conn.execute(text(select_query))
            squad_members = []
            for result in cursor:
                squad_members_dict = {
                    "squad_id": result[0],
                    "player_given_name": result[1],
                    "player_family_name": result[2],
                    "tournament_name": result[3],
                }
                squad_members.append(squad_members_dict)
            cursor.close()
            context = dict(squad_members=squad_members)
            return render_template("squad_members.html", **context)
        except Exception as e:
            print(e)
            return render_template("error.html")
        
    try:
        select_query = f"""SELECT 
                                a1.squad_id, 
                                p1.player_given_name, 
                                p1.player_family_name, 
                                t1.tournament_name
                            FROM 
                                squads a1,
                                players p1,
                                tournaments t1
                            WHERE
                                a1.tournament_id = t1.tournament_id AND
                                a1.squad_id = \'SQ-0001\' AND
                                p1.player_id = ANY(a1.player_ids)"""
        cursor = g.conn.execute(text(select_query))
        squad_members = []
        for result in cursor:
            squad_members_dict = {
                "squad_id": result[0],
                "player_given_name": result[1],
                "player_family_name": result[2],
                "tournament_name": result[3],
            }
            squad_members.append(squad_members_dict)
        cursor.close()
        context = dict(squad_members=squad_members)
        return render_template("squad_members.html", **context)
    except Exception as e:
        print(e)
        return render_template("error.html")
    
from sqlalchemy import text

@app.route("/word_clouds")
def word_clouds():
    football_query = text("""SELECT country_name, ts_rank(to_tsvector('english', countries_wiki_intro), to_tsquery('english', 'football')) AS rank
                             FROM countries
                             WHERE to_tsvector('english', countries_wiki_intro) @@ to_tsquery('english', 'football')
                             ORDER BY rank DESC;""")
    soccer_query = text("""SELECT country_name, ts_rank(to_tsvector('english', countries_wiki_intro), to_tsquery('english', 'soccer')) AS rank
                           FROM countries
                           WHERE to_tsvector('english', countries_wiki_intro) @@ to_tsquery('english', 'soccer')
                           ORDER BY rank DESC;""")

    football_results = g.conn.execute(football_query).fetchall()
    soccer_results = g.conn.execute(soccer_query).fetchall()

    # Convert Row objects to dictionaries
    football_data = [{"country_name": row[0], "rank": row[1]} for row in football_results]
    soccer_data = [{"country_name": row[0], "rank": row[1]} for row in soccer_results]

    context = {
        "football_data": football_data,
        "soccer_data": soccer_data
    }
    return render_template("word_clouds.html", **context)

    
@app.route("/matches")
def matches():
    try:
        select_query = f"""SELECT 
                            match_id,
                            match_name
                            stage_name,
                            group_name,
                            stadium_name,
                            result,
                            score,
                            c1.country_name,
                            c2.country_name,
                            match_date,
                            match_time
                        FROM 
                            matches m1,
                            squads s1,
                            squads s2,
                            countries c1,
                            countries c2
                        WHERE
                            m1.home_squad_id = s1.squad_id AND s1.country_id = c1.country_id AND 
                            m1.away_squad_id = s2.squad_id and s2.country_id = c2.country_id;"""
        cursor = g.conn.execute(text(select_query))
        matches = []
        for result in cursor:
            matches_dict = {
                "match_id": result[0],
                "match_name": result[1],
                #"stage_name": result[4],
                "group_name": result[2],
                "stadium_name": result[3],
                "result": result[4],
                "score": result[5],
                "home_squad": result[6],
                "away_squad": result[7],
                "match_date": result[8],
                "match_time": result[9],
            }
            print(matches_dict)
            matches.append(matches_dict)
        cursor.close()
        print(matches)
        context = dict(matches=matches)
        return render_template("matches.html", **context)
    except Exception as e:
        print(e)
        return render_template("error.html")


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
