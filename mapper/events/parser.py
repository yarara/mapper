from lxml import etree
import sys
import os
from datetime import datetime
from mapper.events.models import Event, Place, Schedule

current_dir = os.path.dirname(os.path.abspath(__file__))


def get_rss():
    file = open('{0}/test.xml'.format(current_dir))
    file_text = file.read()
    file.close()

    return file_text


def get_events(events):
    for event in events:
        event_dict = dict()
        if 'id' in event.attrib.keys():
            event_dict['id'] = event.attrib['id']
        if 'price' in event.attrib.keys():
            event_dict['price'] = event.attrib['price']
        if 'type' in event.attrib.keys():
            event_dict['event_type'] = event.attrib['type']

        title = event.find('title')
        age_restricted = event.find('age_restricted')
        tags = event.find('tags')
        persons = event.find('persons')
        text = event.find('text')
        description = event.find('description')
        stage_theatre = event.find('stage_theatre')
        gallery = event.find('gallery')

        if title  is not None:
            event_dict['title'] = title.text
        if age_restricted  is not None:
            event_dict['age_restricted'] = age_restricted.text
        if tags  is not None:
            event_dict['tags'] = '; '.join([tag.text for tag in tags.findall('tag')])
        if persons  is not None:
            event_dict['persons'] = [{'name': person.find('name').text, 'role': person.find('role').text} for person in persons.findall('person')]
        if text  is not None:
            event_dict['text'] = text.text
        if description  is not None:
            event_dict['description'] = description.text
        if stage_theatre  is not None:
            event_dict['stage_theatre'] = stage_theatre.text
        if gallery is not None:
            event_dict['image_url'] = '; '.join([image.attrib['href'] for image in gallery.findall('image')])

        # print(event_dict.keys())
        # print(event_dict.values())

        new_event = Event()
        for key in event_dict.keys():
            # if hasattr(new_event, key):
            setattr(new_event, key, event_dict[key])
        new_event.save()


def get_places(places):
    for place in places:
        place_dict = dict()
        if 'id' in place.attrib.keys():
            place_dict['id'] = place.attrib['id']
        if 'type' in place.attrib.keys():
            place_dict['place_type'] = place.attrib['type']

        city = place.find('city')
        title = place.find('title')
        address = place.find('address')
        coordinates = place.find('coordinates')
        phones = place.find('phones')
        tags = place.find('tags')
        metros = place.find('metros')
        gallery = place.find('gallery')
        text = place.find('text')
        url = place.find('url')
        work_times = place.find('work_times')

        if city is not None:
            place_dict['city'] = city.text
        if title is not None:
            place_dict['title'] = title.text
        if address is not None:
            place_dict['address'] = address.text
        if coordinates is not None:
            place_dict['latitude'] = coordinates.attrib['latitude']
            place_dict['longitude'] = coordinates.attrib['longitude']
        if phones is not None:
            place_dict['phones'] = '; '.join([phone.text for phone in phones.findall('phone')])
        if tags is not None:
            place_dict['tags'] = '; '.join([tag.text for tag in tags.findall('tag')])
        if metros is not None:
            place_dict['metros'] = '; '.join([metro.text for metro in metros.findall('metro')])
        if gallery is not None:
            place_dict['image_url'] = '; '.join([image.attrib['href'] for image in gallery.findall('image')])
        if text is not None:
            place_dict['text'] = text.text
        if url is not None:
            place_dict['url'] = url.text
        if work_times is not None:
            for work_time in work_times.findall('work_time'):
                if work_time.attrib['type'] == 'kassa':
                    place_dict['work_time_kassa'] = work_time.text
                if work_time.attrib['type'] == 'openhours':
                    place_dict['work_time_openhours'] = work_time.text
                if work_time.attrib['type'] == 'other':
                    place_dict['work_time_other'] = work_time.text

        new_place = Place()
        for key in place_dict.keys():
            if hasattr(new_place, key):
                setattr(new_place, key, place_dict[key])
        new_place.save()


def get_schedule(schedule):
    for session in schedule.findall('session'):
        session_dict = dict()
        session_dict['event_id'] = session.attrib['event']
        session_dict['place_id'] = session.attrib['place']
        session_dict['date'] = datetime.strptime(session.attrib['date'], "%Y-%m-%d").date()
        session_dict['time'] = session.attrib['time']
        if 'timetill' in session.attrib.keys():
            session_dict['timetill'] = session.attrib['timetill']

        # print(session_dict)

        new_session = Schedule()
        for key in session_dict.keys():
            if hasattr(new_session, key):
                setattr(new_session, key, session_dict[key])
        new_session.save()


def parser():
    xml_text = get_rss()

    if sys.version_info.major == 3:
        xml = etree.fromstring(xml_text.encode('utf-8'))
    else:
        xml = etree.fromstring(xml_text)

    events = xml.find('events')
    places = xml.find('places')
    schedule = xml.find('schedule')
    get_events(events)
    get_places(places)
    get_schedule(schedule)

    return 'the creation of records in the database successfully'


