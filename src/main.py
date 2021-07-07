from pygit2 import Repository, GIT_SORT_TOPOLOGICAL
import datetime as dt
import pytz


class workHours:
    def __init__(self) -> None:
        self.morning = 0
        self.afterWork = 0
        self.midNight = 0

    def increment(self, field):
        self.__dict__[field] += 1


class Month:
    def __init__(self) -> None:
        self.weekDays = workHours()
        self.weekends = workHours()

    def addCommit(self, name, hour):
        self.__dict__[name].increment(hour)


class Author:
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.month = [Month() for i in range(6)]

    # TODO: update this debug code
    def __repr__(self) -> str:
        return self.name + ' ' + str(self.month[3].weekDays.midNight)

    def addToWeekDays(self, targetMonth, num):
        self.month[targetMonth].weekDays += num

    def addToWeekends(self, targetMonth, num):
        self.month[targetMonth].weekends += num


def addCollab(list, name, email):

    for i in list:
        if (i.name == name or i.email == email):
            return i

    list.append(Author(name, email))
    return list[len(list) - 1]


def addToCommitHour(month, commitDate):
    if commitDate.weekday() > 4:
        day = 'weekDays'
    else:
        day = 'weekends'

    if commitDate.hour in range(0, 8):
        hour = 'midNight'
    elif commitDate.hour in range(9, 6):
        hour = 'workHours'
    else:
        hour = 'afterWork'

    month.addCommit(day, hour)
    return month


def main():
    # grab the repo name from the user
    repo = Repository('')

    collaraborators = []

    # TODO: set the time zone from env

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

        if(currentMonth > 5):
            break

        coll = addCollab(collaraborators, commit.author.name,
                         commit.author.email)

        # analysis for the work time
        addToCommitHour(coll.month[currentMonth], commitDate)
        # coll.addToWeekDays(currentMonth, 1)

    print(collaraborators)


main()
