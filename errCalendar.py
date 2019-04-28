from errbot import BotPlugin, botcmd

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

        self.calendar = moduleGcalendar.moduleGcalendar()
        self.calendar.setClient('ACC0')
        self.calendar.setCalendarList()

    def get_configuration_template(self):
        """ configuration entries """
        config = {
            'calendar': 'primary',
        }

        return config

    @botcmd
    def cal(self, msg, args):
        if self.config['calendar'] != 'primary':
            self.calendar.active = self.config['calendar']
        else:
            self.calendar.active = 'primary'

        self.calendar.setPosts()
        for i, event in enumerate(self.calendar.getPosts()):
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
            else:
                line = line + 'Busy'

            yield(line)

        yield end()

