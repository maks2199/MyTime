import icalendar

e = open('10_Input_calendars/tachkov.maksim@gmail.com.ics', 'rb')
ecal = icalendar.Calendar.from_ical(e.read())
for component in ecal.walk():
    if component.name == "VEVENT":
        print(component.get("summary"))
        # print(component.get("description"))
        # print(component.get("organizer"))
        # print(component.get("location"))
        print(component.decoded("dtstart"))
        print(component.decoded("dtend"))
e.close()
