![kicktipp-img]

[kicktipp-img]: https://www.kicktipp.de/assets/img/cb1059167120/assets/img/illu/startseite.png "Kicktipp"

kicktipp-betbot
===============

A tool to palce bets on www.kicktipp.de automatically

kicktipp-betbot is a python based command-line tool that will place bets on www.kicktipp.de for you.

Motivation
----------

I sometimes forget to place bets for the upcomming matchday. Therefore I wanted to create a 'simple' tool that places bets on the matchday right before the deadline.

Getting started
---------------

The tool is designed as python command-line application and is intended to be used in conjunction with e.g. cron jobs.
It is also possible to use it interactively.

The main goal is to use this betbot non interactivly, therefore two steps are required to get it work.

1. Generate a login token for later use
2. Call the betbot with the generated login token

### Generate a login token
If yout dont want to use the betbot interactively you must generate a login token.
The first task is to generate a login token. Fortunately the kicktipp website provides a login cookie that is used for this purpose.

```console
$ kicktippbb.py --get-login-token
Username: myuser@mymail.com
Password: ********
```
The result is a character seqence that is used as logint token for further requests.

### Place bets
In order to let the tool place bets for you just invoke it and pass it the generated login token.
It will use the token and navigate to the 'tippabgabe' sub URL where the bets for the next matchday are placed.
The result will be shown on the console.

```console
$ kicktippbb.py --use-login-token c3HfazFh6sd
Community: testspiel
02.10.2020 20:30 '1. FC Union Berlin' vs. 'FSV Mainz 05'  (2.15;3.5;3.3) - betting 1:2
03.10.2020 15:30 'VfB Stuttgart' vs. 'Bayer 04 Leverkusen'  (3.0;3.75;2.2) - betting 1:0
03.10.2020 15:30 'Eintracht Frankfurt' vs. '1899 Hoffenheim'  (2.8;3.75;2.35) - betting 1:1
03.10.2020 15:30 '1. FC Köln' vs. 'Bor. Mönchengladbach'  (3.9;3.9;1.87) - betting 2:0
03.10.2020 15:30 'Werder Bremen' vs. 'Arminia Bielefeld'  (2.15;3.6;3.3) - betting 3:1
03.10.2020 15:30 'Borussia Dortmund' vs. 'SC Freiburg'  (1.4;5.0;7.25) - betting 3:1
03.10.2020 18:30 'RB Leipzig' vs. 'FC Schalke 04'  (1.3;5.75;9.0) - betting 3:0
04.10.2020 15:30 'VfL Wolfsburg' vs. 'FC Augsburg'  (1.91;3.75;3.8) - betting 2:1
04.10.2020 18:00 'FC Bayern München' vs. 'Hertha BSC'  (1.14;9.25;16.5) - betting 3:1
```

All of your bet communities will be considered by the tool unless you specifiy the desired communities.

```console
$ kicktippbb.py --use-login-token c3HfazFh6sd mycommunityname
...
```

### Taming the daemon
Some useful options to tweak the behavior of the betbot.

#### Deadline:
If you want the betbot to pick up the slack only in the last minute, there are some options you might consider using.
```console
$ kicktippbb.py --use-login-token c3HfazFh6sd --dealine 10m mycommunityname
...
04.10.2020 18:00 'FC Bayern München' vs. 'Hertha BSC'  (1.17;10.0;21.0) - not betting yet, due in 00:37
...
```

#### Override:
By default the betbot doesn't override bets you already placed. So you may see an output like this:
```console
$ kicktippbb.py --use-login-token c3HfazFh6sd  mycommunityname
...
04.10.2020 18:00 'FC Bayern München' vs. 'Hertha BSC'  (1.16;8.5;14.5) - skipped, already placed 3:1
...
```
Specifying the ```--overide-bets``` option will ignore already placed bets and override former placed bets.

#### Matchday
If you like to place bets on a specific matchday you can use the ```--matchday``` option.
This comes in handy if a match is postponed and kicktipp.de just navigates to the matchday with the postponed open match instead of the current matchday.
You can specify any matchday betweeen 1 and 34.
```console
$ kicktippbb.py --matchday=12 mycommunityname
...
```

#### Testing the outcome:
If you don't want the betbot to carry out any operations on your games you can add the ```--dry-run``` parameter. This prevents the betbot from submitting any bets to your prediction games.

### Match Predictor Functions
By default the betbot uses a rather simple prediction algorithm called 'SimplePredictor'. You can specify a predictor method by using the ```--predictor <predictorname>``` parameter.

```console
$ kicktippbb.py --use-login-token c3HfazFh6sd --predictor CalculationPredictor mycommunityname
...
```

The prediction functions reside in the predition.py module and can be extended at will. The name of the function must match the parameter value, it will be looked up in the module and used for match result prediciton.

### Usage 

Here the usage:
```console
$ kicktippbb.py --help
KickTipp BetBot
Automated kicktipp.de bet palcement.

Places bets to the upcomming matchday.
Unless specified by parameter it places the bets on all prediction games of the account.

Usage:
    kicktippbb.py [ --get-login-token ]
    kicktippbb.py [ --list-predictors ]
    kicktippbb.py [--use-login-token <token> ] [--dry-run] [--override-bets] [--deadline <duration>] [--predictor <value>] [--matchday <value>] [COMMUNITY]...

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
    --dry-run                   Dont place any bet just print out predicitons
    --matchday <value>          Choose a specific matchday in the range of 1 to 34 to place bets on  
```