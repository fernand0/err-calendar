from errbot import BotPlugin, botcmd
from errbot.templating import tenv
from dateutil.parser import parse

import moduleGcalendar
# https://github.com/fernand0/scripts/blob/master/moduleGcalendar.py

def end(msg=""):
    return("END"+msg)

class ErrCalendar(BotPlugin):    
        
    def activate(self):
        """
        Triggers on plugin activation
        You should delete it if you're not using it to override any default behaviour
        """
        super(ErrCalendar, self).activate()

        self.calendar = {}
        self.accounts = ['ACC0', 'ACC1']
        for name in self.accounts:
            cal = moduleGcalendar.moduleGcalendar()
            cal.setClient(name)
            cal.setCalendarList()

            #if self.config['calendar'] != 'primary':
            #    cal.active = self.config['calendar']
            #else:
            cal.active = 'primary'
            self.calendar[name] = cal

    def get_configuration_template(self):
        """ configuration entries """
        config = {
            'calendar': 'primary',
        }

        return config

    @botcmd
    def listCal(self, msg, args):
        #for i, cal in enumerate(filter(lambda x: args.lower() 
        #             n x['summary'].lower(), self.calendar.getCalendarList())):
        for acc in self.calendar:
            yield acc
            for i, cal in enumerate(self.calendar[acc].getCalendarList()):
                if args.lower() in cal['summary'].lower():
                    line = "%d) %s" % (i, cal['summary'])
                    yield(line)
        yield end()

    @botcmd
    def selCal(self, msg, args):
        if args.find(' ')>0:
            argsS = args.split(' ')
            if (len(argsS) == 3):
                date = argsS[2]
                whichCal = argsS[0]
                argsL = argsS[1]
            elif(len(argsS) == 2):
                whichCal = argsS[0]
                argsL = argsS[1]
        else:
            argsL = args
            whichCal = '012' 

        if args:
            myCal = None
            for i, acc in enumerate(self.calendar):
                # Acc : ACC0, ACC1
                if (str(i) in whichCal):
                    cal = self.calendar[acc]
                    if argsL.isdigit():
                        myCal = cal.getCalendarList()[int(argsL)]
                    else:
                        for c in cal.getCalendarList():
                            if argsL in c['summary']: 
                                myCal = c
                                break
            if myCal:
                yield "Selected %s" % myCal['summary']
                cal.setActive(myCal['id'])
            for ca in self.cal(msg, args):
                yield ca
        yield end()

    @botcmd
    def showCal(self, msg, args):
        for cal in  self.cal(msg, args):
            yield cal
        yield end()
         
    def cal(self, msg, args):
        if args.find(' ')>0:
            argsS = args.split(' ')
            if (len(argsS) == 3):
                date = argsS[2]
                whichCal = argsS[0]
                argsL = argsS[1]
            elif(len(argsS) == 2):
                date = ''
                whichCal = argsS[1]
                argsL = argsS[0]
        else:
            date = ''
            argsL = args
            whichCal = '012' 

        for i, acc in enumerate(self.calendar):
            if str(i) in whichCal:
                cal = self.calendar[acc]
                cal.setPosts(date)
                yield cal.nick
                updates = []
                for i, event in enumerate(cal.getPosts()):
                    line = "%d) " % i
                    if 'start' in event:
                        if 'dateTime' in event['start']:
                            dateS = event['start']['dateTime']
                            import dateutil.parser
                            dateSD = dateutil.parser.parse(dateS)
                            dateE = event['end']['dateTime']
                            newDateE = ''
                            eq = 0
                            for i, char in enumerate(dateE):
                                if dateS[i] != dateE[i]:
                                    newDateE = newDateE + dateE[i]
                                    eq = 1
                                elif eq == 1:
                                    break
                            line = "%s %s, %d %d:%02d (%s) " % (line, dateSD.strftime("%a"), dateSD.day, dateSD.hour, dateSD.minute, newDateE)
                            #line = line + ' ' + dateSD.day+' '+dateSD.hour+':'+dateSD.minute + ' (Ends at ' + newDateE + ') '
                        elif 'date' in event['start']:
                            line = line + ' ' +event['start']['date'] + ' (Ends at ' + event['end']['date']+')'
                    if 'summary' in event:
                        line = line + event['summary']
                        update = (dateSD.strftime("%a"), dateSD.day, dateSD.hour, dateSD.minute, newDateE, event['summary'])
                    else:
                        line = line + 'Busy'
                        update = (dateSD.strftime("%a"), dateSD.day, dateSD.hour, dateSD.minute, newDateE, 'Busy')
                    updates.append(update)

                    #yield(line)

                response = tenv().get_template('calendar.md').render({'updates': updates})
                yield response
