import copy
import icalendar as ical

all_deadline_descriptions = {
    "absentee.postmarked_by": "Absentee ballots postmarked in {}",
    "absentee.received_by": "Absentee ballots received in {}",
    "absentee.in_person_by": "Hand deliver absentee ballots in {}",
    "absentee.application.postmarked_by": "Absentee applications postmarked in {}",
    "absentee.application.received_by": "Absentee applications received in {}",
    "absentee.application.in_person_by": "Hand deliver absentee applications in {}"
}

deadline_descriptions = {
    "absentee.postmarked_by": "Mail ballot at the post office!",
    "absentee.received_by": "Last day for election officials to receive your absentee ballot. Mail early!",
    "absentee.in_person_by": "Drop off ballot in person!",
    "absentee.application.postmarked_by": "Mail absentee application at the post office!",
    "absentee.application.received_by": "Last day for election officials to receive your absentee application. Mail early!",
    "absentee.application.in_person_by": "Drop off absentee application in person!"
}

def generate(dates, output_filename, *, name=None, description=None, uid=None, states=None, counties=None):
    c = ical.Calendar()
    c.add("prodid", "-//electioncal.us generator//circuitpython.org//")
    c.add("version", "2.0")
    path_parts = output_filename.split("/")
    c.add(
        "url", ical.vUri("https://electioncal.us/" + "/".join(path_parts[1:-1]) + "/")
    )
    c.add("source", ical.vUri("https://electioncal.us/" + "/".join(path_parts[1:])))
    # c.add('REFRESH-INTERVAL'VALUE=DURATION:P1W, value)
    if name:
        c.add("name", name)
    if description:
        c.add("description", description)
    if uid:
        c.add("uid", uid)

    last_modified = None
    for date in dates:
        date = copy.deepcopy(date)
        name = None
        if date["state"] and states:
            name = states[date["state"]]["name"]
        elif date["county"] and counties:
            name = counties[date["county"]]["name"]
        if date["type"] == "deadline":
            if name:
                desc = all_deadline_descriptions.get(date["subtype"], None)
                if not desc:
                    print("missing description for", date["subtype"])
                else:
                    date["name"] = desc.format(name)
            else:
                desc = deadline_descriptions.get(date["subtype"], None)
                if not desc:
                    print("missing description for", date["subtype"])
                else:
                    date["name"] = desc
        elif date["type"] == "election" and name:
            date["name"] = name + " " + date["name"]
        event = ical.Event()
        event.add("summary", date["name"])
        event.add("dtstart", ical.vDate(date["date"]))
        c.add_component(event)

    if description:
        c.add("last-modified", ical.vDate(date["date"]))

    with open(output_filename, "wb") as f:
        f.write(c.to_ical())


# def add_holiday_notice(calendar, d, note):
#     d = localize(d)

# def add_meeting_notice(calendar, d, note):
#     d = localize(d)
#     event = icalendar.Event()
#     event.add('summary', 'CircuitPython Discord Meeting' + note)
#     event.add('dtstart', icalendar.vDatetime(d))
#     event.add('dtend', icalendar.vDatetime(d + meeting_duration))
#     event.add('dtstamp', icalendar.vDatetime(now))
#     if 0:  # This doesn't work, makes google not show the calendar at all
#         event.add('conference',
#                   'https://adafru.it/discord',
#                   parameters= {'VALUE':'URI'})
#     calendar.add_component(event)
