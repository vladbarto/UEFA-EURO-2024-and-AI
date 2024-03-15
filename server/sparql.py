# insert all sparql code here
from string import Template
from SPARQLWrapper import SPARQLWrapper, JSON
'''
all queries defined by Ly wrapped into sparql queries
-> call by need in flask routes
'''
fuseki_path = "http://localhost:3030/football/"


def which_teams_participate_query():
    sparql = SPARQLWrapper(fuseki_path)
    sparql.setReturnFormat(JSON)
    query_string = """
    PREFIX : <https://www.h-da.de/>
    SELECT ?teamName
    WHERE {
       ?team a :Team .
       ?team :name ?teamName .
    }
    """
    sparql.setQuery(query_string)
    results_dict = sparql.query().convert()
    return [row['teamName']['value'] for row in results_dict['results']['bindings']]


def who_is_the_coach_of_x_query(team_x):
    sparql = SPARQLWrapper(fuseki_path)
    sparql.setReturnFormat(JSON)
    query = """
    PREFIX : <https://www.h-da.de/>
    SELECT ?coachName
    WHERE {
       ?team a :Team ;
         :name "$team_x" ; #change name of the team here
             :coach ?coach .
       ?coach :name ?coachName .
    }
    """
    query_string = Template(query).substitute(team_x=team_x)
    sparql.setQuery(query_string)
    results_dict = sparql.query().convert()
    return results_dict['results']['bindings'][0]['coachName']['value']


def who_is_in_the_team_of_x(team_x):
    sparql = SPARQLWrapper(fuseki_path)
    sparql.setReturnFormat(JSON)
    query = """
    PREFIX : <https://www.h-da.de/>
    SELECT ?playerName
    WHERE {
       ?team a :Team ;	
         :name "$team_x" ; #change name of the team here
             :player ?player .
       ?player :name ?playerName .
    }
    """
    query_string = Template(query).substitute(team_x=team_x)
    sparql.setQuery(query_string)
    results_dict = sparql.query().convert()
    return [[row['playerName']['value']] for row in results_dict['results']['bindings']]


def custom_match_list_of_x(team_x):
    sparql = SPARQLWrapper(fuseki_path)
    sparql.setReturnFormat(JSON)
    query = """
    PREFIX : <https://www.h-da.de/>
    SELECT ?matchSchedule ?matchDate ?matchVenue (MIN(?opponentName) as ?opponent)
    WHERE {
       ?match a :Match ;
              :schedule ?matchSchedule ;
              :date ?matchDate ;
              :venue ?venue ;
              :participant ?team1, ?team2 .
       ?venue :name ?matchVenue
       {
          ?team1 :name "$team_x" . #change team name here
          ?team2 :name ?opponentName .
       }
       UNION
       {
          ?team2 :name "$team_x" . #change team name here
          ?team1 :name ?opponentName .
       }
       FILTER(?opponentName != "$team_x") #change team name here
    }
    GROUP BY ?match ?matchSchedule ?matchDate ?matchVenue
    """
    query_string = Template(query).substitute(team_x=team_x)
    sparql.setQuery(query_string)
    results_dict = sparql.query().convert()
    return [[row['matchSchedule']['value'],
            row['matchDate']['value'],
            row['matchVenue']['value'],
            row['opponent']['value']] for row in results_dict['results']['bindings']]
    return [results_dict['results']['bindings'][0]['matchSchedule']['value'],
            results_dict['results']['bindings'][0]['matchDate']['value'],
            results_dict['results']['bindings'][0]['matchVenue']['value'],
            results_dict['results']['bindings'][0]['opponent']['value']
    ]

def information_about_coach_x(person_x):
    sparql = SPARQLWrapper(fuseki_path)
    sparql.setReturnFormat(JSON)
    query = """
    PREFIX : <https://www.h-da.de/>
    SELECT ?coachName ?dob ?nationality
WHERE {
   ?coach a :Coach ;
          :name "$person_x" ; #change name here
          :date_of_birth ?dob ;
          :nationality ?nationality .
}
"""
    query_string = Template(query).substitute(person_x=person_x)
    sparql.setQuery(query_string)
    results_dict = sparql.query().convert()
    return [results_dict['results']['bindings'][0]['dob']['value'], results_dict['results']['bindings'][0]['nationality']['value']]


def information_about_player_x(person_x):
    sparql = SPARQLWrapper(fuseki_path)
    sparql.setReturnFormat(JSON)
    query = """
PREFIX : <https://www.h-da.de/>
SELECT ?playerName ?dob ?nationality ?position
WHERE {
   ?player a :Player ;
           :name "$person_x" ; #insert name here
           :date_of_birth ?dob ;
           :nationality ?nationality ;
           :position ?position .
}
    """
    query_string = Template(query).substitute(person_x=person_x)
    sparql.setQuery(query_string)
    results_dict = sparql.query().convert()
    return [results_dict['results']['bindings'][0]['dob']['value'],
            results_dict['results']['bindings'][0]['nationality']['value'],
            results_dict['results']['bindings'][0]['position']['value']
    ]


def how_many_players_in_team_x(team_x):
    sparql = SPARQLWrapper(fuseki_path)
    sparql.setReturnFormat(JSON)
    query = """
    PREFIX : <https://www.h-da.de/>
    SELECT (COUNT(?player) as ?playerCount)
    WHERE {
       ?team a :Team ;
         :name "$team_x" ; #change team name here
             :player ?player .
    }"""
    query_string = Template(query).substitute(team_x=team_x)
    sparql.setQuery(query_string)
    results_dict = sparql.query().convert()
    return results_dict['results']['bindings'][0]['playerCount']['value']


def who_plays_as_role_in_team_x(input_tuple):
    # x==team
    # y==position
    x = input_tuple[0]
    y = input_tuple[1]
    sparql = SPARQLWrapper(fuseki_path)
    sparql.setReturnFormat(JSON)
    query = """
    PREFIX : <https://www.h-da.de/>
    SELECT ?playerName
    WHERE {
       ?team a :Team ;
         :name "Spain" ; #change team name here
             :player ?player .
       ?player :position "Goalkeeper" ; #change position here
               :name ?playerName .
    }
    """
    # query_string = Template(query).substitute(team=input_tuple[0])
    # query_string = Template(query).substitute(role=y)
    # sparql.setQuery(query_string)
    results_dict = sparql.query().convert()
    return results_dict['results']['bindings'][0]['playerName']['value']


def where_is_stadium_x_located(x):
    sparql = SPARQLWrapper(fuseki_path)
    sparql.setReturnFormat(JSON)
    query = """
    PREFIX : <https://www.h-da.de/>
    SELECT ?stadiumName ?location
    WHERE {
       ?stadium a :Venue ;
                :name "$arena" ; #change stadium name here
                :ort ?location .
    }
    """
    query_string = Template(query).substitute(arena=x)
    sparql.setQuery(query_string)
    results_dict = sparql.query().convert()
    return results_dict['results']['bindings'][0]['location']['value']


def description_of_team_x(x):
    sparql = SPARQLWrapper(fuseki_path)
    sparql.setReturnFormat(JSON)
    query = """
    PREFIX : <https://www.h-da.de/>
    SELECT ?description
WHERE {
   ?subject a :Team ; 
            :name "$team" ; #change team name here
            :description ?description .
}
    """
    query_string = Template(query).substitute(team=x)
    sparql.setQuery(query_string)
    results_dict = sparql.query().convert()
    return results_dict['results']['bindings'][0]['description']['value']


def group_stage_matches_venues_and_capacities():
    sparql = SPARQLWrapper(fuseki_path)
    sparql.setReturnFormat(JSON)
    query = """
    PREFIX : <https://www.h-da.de/>
    SELECT ?venueName ?capacity
    WHERE {
       ?match a :Match;
              :venue ?venue.
       ?venue :name ?venueName;
              :capacity ?capacity.
    }
    """
    sparql.setQuery(query)
    results_dict = sparql.query().convert()
    return [[row['venueName']['value'], row['capacity']['value']] for row in results_dict['results']['bindings']]