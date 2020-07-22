"""KickTipp BetBot 
Automated kicktipp.de bet palcement.

Places bets to the upcomming matchday.  
Unless specified by parameter it places the bets on all prediction games of the account.

Usage: 
    kicktippbb.py [ --get-login-token ]
    kicktippbb.py [ --list-predictors ]
    kicktippbb.py [--use-login-token <token> ] [--override-bets] [--deadline <duration>] [--predictor <value>] [COMMUNITY]...

Options:
    COMMUNITY                   Name of the prediction game comunity to place bets, 
                                one or more names ca be specified
    --get-login-token           Just login and print the login token string 
                                for later use with '--use-login-token' option
    --use-login-token <token>   Perform bets without interactive login, use login token insted.
    --override-bets             Override already placed bets.
    --deadline <duration>       Place bets only on matches starting within the given duration.                                
                                The duration format is <number><unit[m,h,d]>, e.g. 10m,5h or 1d
    --list-predictors           Display a list of predictors available to be used with '--predictor' option
    --predictor <value>         A specific predictor name to be used during calculation
"""
from robobrowser import RoboBrowser
from bs4 import BeautifulSoup
from docopt import docopt
import getpass
import math
import re
import sys
from match import Match
import more_itertools
import prediction
import inspect

URL_BASE = 'http://www.kicktipp.de'
URL_LOGIN = URL_BASE + '/info/profil/login'

DEADLINE_REGEX = re.compile('([1-9][0-9]*)(m|h|d)')

def login(browser: RoboBrowser):
    """Log into the user account by asking for username and password.
    If login succeded the login cookie token is returned
    """
    while True:
        username, password = get_credentials()
        perform_login(browser, username, password)
        if not logged_in(browser):
            print("Email or password incorrect. Please try again.\n")
        else:
            return browser.session.cookies['login']

def perform_login(browser: RoboBrowser, username:str, password:str):
    """
    Open the log in page then fill out the form and submit 
    """
    browser.open(URL_LOGIN)
    form = browser.get_form()
    form['kennung'] = username
    form['passwort'] = password
    browser.submit_form(form)

def get_credentials():
    """
    Ask the user for the credentials.
    """
    username = input("Username: ")
    password = getpass.getpass(prompt='Password: ')
    return username, password      
                
def logged_in(browser: RoboBrowser):
    """
    Returns true if we are still on the login page
    """
    login_div = browser.find('div', content="Login")
    return True if not login_div else False

def get_table_rows(soup):
    """
    Get all table rows from the first tbody element found in soup parameter
    """
    tbody=soup.find('tbody')
    return [tr.find_all('td') for tr in tbody.find_all('tr')]

def fetch_matches(browser: RoboBrowser, community):
    """Fetch latest odds for each match"""
    browser.open(URL_BASE + '/' + community + '/tippabgabe')
    
    content = get_kicktipp_content(browser)
    rows = get_table_rows(content)
    matches = [Match(row[1].get_text(), row[2].get_text(), row[0].get_text(), row[4].get_text(), row[5].get_text(), row[6].get_text()) for row in rows]
    for m1, m2 in more_itertools.pairwise(matches):
        if not m2.match_date:
            m2.match_date = m1.match_date

    return matches


def get_kicktipp_content(browser: RoboBrowser):
    """
    Get the content view area from the kicktipp page.
    """
    content = browser.find_all(id='kicktipp-content')
    if content[0]:
        return content[0]
    return None


def get_communities(browser: RoboBrowser , desired_communities: list):
    """
    Get a list of all communities of the user
    """
    browser.open(URL_BASE + '/info/profil/meinetipprunden')
    content = get_kicktipp_content(browser)
    links = content.find_all('a')
    is_community = lambda link: link.get('href').replace("/","") == link.get_text()
    community_list = [link.get_text() for link in links if is_community(link)]
    if len(desired_communities) > 0:
        return intersection(community_list, desired_communities)
    return community_list

def intersection(a, b):
    i = [x for x in a if x in b]
    return i

def place_bets(browser: RoboBrowser, communities:list, predictor, override=False, deadline=None):
    """Place bets on all given urls."""
    for com in communities:
        matches = fetch_matches(browser, com)
        for match in matches:
            tip = predictor.predict(match)
            print("{0} - {1} ({2};{3};{4})  {5}:{6}".format(match.hometeam, match.roadteam, match.rate_home, match.rate_deuce, match.rate_road, tip[0], tip[1]))            

    #TODO: Fill the forms with the game prediction
    #TODO: Consider bet placement timeout
    #TODO: Consider override parameter


def validate_arguments(arguments):
    if arguments['--deadline']:
        deadline_value = arguments['--deadline']
        
        if not re.match(DEADLINE_REGEX, deadline_value):            
            exit("Invalid deadline value ({}), use <Number><Unit>, Unit=[m,h,d]".format(deadline_value))

def choose_predictor(predictor_param, predictors):
    if(predictor_param):         
        if(predictor_param in predictors):
            predictor = predictors[predictor_param]()
        else:
            exit ('Unknown predictor: {}'.format(predictor_param))
    else:
        predictor = predictors['SimplePredictor']()
    return predictor
    

def get_predictors():
    return dict( (name, obj) for name, obj in inspect.getmembers(sys.modules['prediction'], predicate=inspect.isclass) if 'predict' in [x for x,y in inspect.getmembers(obj, predicate=inspect.isfunction) if x == 'predict'])


def main(arguments):
    browser = RoboBrowser(parser="html.parser")
    
    validate_arguments(arguments)
    predictors = get_predictors()

    # Log in to kicktipp and print out the login cookie value
    if arguments['--get-login-token']:
        token = login(browser)
        print(token)
        exit()
    
    # Just list the predictors at hand and exit
    if arguments['--list-predictors']:
        [print(key) for key in predictors.keys()]
        exit()

    # Use login token pass by argument or let the caller log in right here
    if arguments['--use-login-token']:
        token = arguments['--use-login-token']
    else:
        token = login(browser)

    communities = arguments['COMMUNITY']
    #Just use the token for all interactions with the website
    browser.session.cookies['login'] = token
    
    # Which communities are considered, fail if no were found
    communities = get_communities(browser, communities)
    if(len(communities) == 0):
        exit("No community found!?")
        
    # Which prediction method is used
    predictor_param = arguments['--predictor'] if '--predictor' in arguments else None
    predictor = choose_predictor(predictor_param, predictors)

    # Place bets
    place_bets(browser, communities, predictor, override=arguments['--override-bets'], deadline=arguments['--deadline'])
            

if __name__ == '__main__':
    arguments = docopt(__doc__, version='KickTipp BetBot 1.0')
    main(arguments)    
