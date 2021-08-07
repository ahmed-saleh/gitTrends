from click.types import STRING
from pygit2 import Repository, GIT_SORT_TOPOLOGICAL, discover_repository
import datetime as dt
import pytz
import click, jsonpickle
from jinja2 import Environment, PackageLoader
import os, webbrowser
import calendar


class workHours:
    def __init__(self) -> None:
        self.morning = 0
        self.afterWork = 0
        self.midNight = 0

    def increment(self, field):
        self.__dict__[field] += 1


class Month:
    def __init__(self):
        self.weekDays = workHours()
        self.weekends = workHours()
        self.total_per_month = 0
        self.month_name = ''

    def addCommit(self, name, hour):
        self.__dict__[name].increment(hour)
        self.total_per_month +=1

    def setMonthName(self, name):
        self.month_name = name


class Author:
    def __init__(self, name, email, months_range):
        self.name = name
        self.email = email
        self.month = [Month() for i in range(months_range)]

    # # TODO: update this debug code
    # def __repr__(self) -> str:
    #     return self.name + ' ' + str(self.month[3].weekDays.midNight)

    def addToWeekDays(self, targetMonth, num):
        self.month[targetMonth].weekDays += num

    def addToWeekends(self, targetMonth, num):
        self.month[targetMonth].weekends += num

# adding of a collaborators without duplicating
def addCollab(list, name, email, months_range):

    for i in list:
        if (i.name == name or i.email == email):
            return i

    list.append(Author(name, email, months_range))
    return list[len(list) - 1]


# adding the hour to the correct bucket
def addToCommitHour(month, commitDate):
    #TODO: verify this logic
    if commitDate.weekday() > 4:
        day = 'weekends'
    else:
        day = 'weekDays'

    if commitDate.hour in range(0, 8):
        hour = 'midNight'
    elif commitDate.hour in range(9, 6):
        hour = 'workHours'
    else:
        hour = 'afterWork'

    month.addCommit(day, hour)
    return month

##
# script start
##
def analyse(value, months_range):
    repo = Repository(value)
    collaraborators = []

    # TODO: set the time zone from env
    # TODO: support accross years analysis
    currentMonth = 0
    setFirst = False
    for commit in repo.walk(repo.head.target, GIT_SORT_TOPOLOGICAL):
        commitDate = dt.datetime.fromtimestamp(
            commit.commit_time, pytz.timezone('Asia/Kuala_Lumpur'))
        if setFirst == False:
            inLoopMonth = commitDate.month
            setFirst = True

        if inLoopMonth > commitDate.month:
            currentMonth += 1
            inLoopMonth = commitDate.month

        if(currentMonth > (months_range -1)):
            break

        coll = addCollab(collaraborators, commit.author.name,
                         commit.author.email, months_range)

        #set the month name
        coll.month[currentMonth].setMonthName(calendar.month_name[commitDate.month])
        # analysis for the work time
        addToCommitHour(coll.month[currentMonth], commitDate)

    output = jsonpickle.encode(collaraborators, unpicklable=False)
    # TODO: make the port variable
    root = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(root, 'output', 'index.html')

    # filename = os.path.join(root, 'html', 'index.html')
    env = Environment(loader=PackageLoader(__name__))
    template = env.get_template('index.html')
    with open(filename, 'w') as fh:
        fh.write(template.render(
            h1 = "Results",
            data=jsonpickle.decode(output),
            repo_name=repo.describe
        ))

    webbrowser.open('file://' + os.path.realpath(filename))

    print('done');


@click.command()
@click.argument("path", type=STRING)
@click.option('--m', '-months', default=6)


def cli(path, m):
    repo_path = discover_repository(path)
    if not repo_path:
        return click.echo('please type a valid git repo path')
    else:
        analyse(path, m)

if __name__ == '__main__':
    cli()
