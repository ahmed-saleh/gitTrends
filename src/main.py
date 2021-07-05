from pygit2 import Repository, GIT_SORT_TOPOLOGICAL
import datetime as dt
import pytz

class Author:
  def __init__(self, name, email):
    self.name = name
    self.email = email
    self.month = [self.Month()  for i in range(6)] 

  #TODO: update this debug code
  def __repr__(self) -> str:
    return self.name + ' ' + str(getattr(self.month[3], 'weekDays'))


  class Month:
    def __init__(self) -> None:
        self.weekDays = 0
        self.weekends = 0

    def __setattr__(self, name, value):
      self.__dict__[name] = value
  

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


def main(): 
    #grab the repo name from the user
    repo = Repository('')

    collaraborators = []

    #TODO: set the time zone from env

    currentMonth = 0
    setFirst = False
    for commit in repo.walk(repo.head.target, GIT_SORT_TOPOLOGICAL):
      if setFirst == False: 
        inLoopMonth = dt.datetime.fromtimestamp(commit.commit_time, pytz.timezone('Asia/Kuala_Lumpur')).month
        print(dt.datetime.fromtimestamp(commit.commit_time, pytz.timezone('Asia/Kuala_Lumpur')))
        setFirst = True

      if inLoopMonth > dt.datetime.fromtimestamp(commit.commit_time, pytz.timezone('Asia/Kuala_Lumpur')).month: 
        print(dt.datetime.fromtimestamp(commit.commit_time, pytz.timezone('Asia/Kuala_Lumpur')).month)
        currentMonth += 1
        inLoopMonth  = dt.datetime.fromtimestamp(commit.commit_time, pytz.timezone('Asia/Kuala_Lumpur')).month

      if(currentMonth > 5): break

      coll = addCollab(collaraborators, commit.author.name, commit.author.email)
      coll.addToWeekDays(currentMonth, 1)


    # for x in collaraborators:
      # print (x.month[2].weekDays)
    print(collaraborators)

main()