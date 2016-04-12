from lxml import etree
import sys
from datetime import datetime
# from mapper.events.models import Event, Place, Schedule

file = open('/home/yaraat/projects/mapper/mapper/test.xml')
file_text = file.read()
file.close()

if sys.version_info.major == 3:
    xml = etree.fromstring(file_text.encode('utf-8'))
else:
    xml = etree.fromstring(file_text)

events = xml.find('events')
places = xml.find('places')
schedule = xml.find('schedule')

for event in events:
    event_dict = dict()
    if 'id' in event.attrib.keys():
        event_dict['id'] = event.attrib['id']
    if 'price' in event.attrib.keys():
        event_dict['price'] = event.attrib['price']
    if 'type' in event.attrib.keys():
        event_dict['event_type'] = event.attrib['type']
    if event.find('title'):
        event_dict['title'] = event.find('title').text
    if event.find('age_restricted'):
        event_dict['age_restricted'] = event.find('age_restricted').text
    if event.find('tags'):
        event_dict['tags'] = '; '.join([tag.text for tag in event.find('tags').findall('tag')])
    if event.find('persons'):
        event_dict['persons'] = [{'name': person.find('name').text, 'role': person.find('role').text} for person in event.find('persons').findall('person')]
    if event.find('text'):
        event_dict['text'] = event.find('text').text
    if event.find('description'):
        event_dict['description'] = event.find('description').text
    if event.find('stage_theatre'):
        event_dict['stage_theatre'] = event.find('stage_theatre')
    if event.find('gallery'):
        event_dict['image_url'] = '; '.join([image.attrib['href'] for image in event.find('gallery').findall('image')])

    print(event_dict.keys())
    print(event_dict.values())

    # new_event = Event()
    # for key in event_dict.keys():
    #     # if hasattr(new_event, key):
    #     setattr(new_event, key, event_dict[key])
    # new_event.save()

for place in places:
    place_dict = dict()
    if 'id' in place.attrib.keys():
        place_dict['id'] = place.attrib['id']
    if 'type' in place.attrib.keys():
        place_dict['place_type'] = place.attrib['type']
    if place.find('city'):
        place_dict['city'] = place.find('city').text
    if place.find('title'):
        place_dict['title'] = place.find('title').text
    if place.find('address'):
        place_dict['address'] = place.find('address').text
    if place.find('coordinates'):
        place_dict['latitude'] = place.find('coordinates').attrib['latitude']
        place_dict['longitude'] = place.find('coordinates').attrib['longitude']
    if place.find('phones'):
        place_dict['phones'] = '; '.join([phone.text for phone in place.find('phones').findall('phone')])
    if place.find('tags'):
        place_dict['tags'] = '; '.join([tag.text for tag in place.find('tags').findall('tag')])
    if place.find('metros'):
        place_dict['metros'] = '; '.join([metro.text for metro in place.find('metros').findall('metro')])
    if place.find('gallery'):
        place_dict['image_url'] = '; '.join([image.attrib['href'] for image in place.find('gallery').findall('image')])
    if place.find('text'):
        place_dict['text'] = place.find('text').text
    if place.find('url'):
        place_dict['url'] = place.find('url').text
    if place.find('work_times'):
        for work_time in place.find('work_times').findall('work_time'):
            if work_time.attrib['type'] == 'kassa':
                place_dict['work_time_kassa'] = work_time.text
            if work_time.attrib['type'] == 'openhours':
                place_dict['work_time_openhours'] = work_time.text
            if work_time.attrib['type'] == 'other':
                place_dict['work_time_other'] = work_time.text

    print(place_dict)
    # new_place = Place()
    # for key in place_dict.keys():
    #     if hasattr(new_place, key):
    #         setattr(new_place, key, place_dict[key])
    # new_place.save()

for session in schedule.findall('session'):
    session_dict = dict()
    session_dict['event'] = session.attrib['event']
    session_dict['place'] = session.attrib['place']
    session_dict['date'] = datetime.strptime(session.attrib['date'], "%Y-%m-%d").date()
    session_dict['time'] = session.attrib['time']
    if 'timetill' in session.attrib.keys():
        session_dict['timetill'] = session.attrib['timetill']

    print(session_dict)

    # new_session = Schedule()
    # for key in session_dict.keys():
    #     if hasattr(new_session, key):
    #         setattr(new_session, key, session_dict[key])
    # new_session.save()


# def print_elem(xml):
# 	if xml.getchildren():
# 		for children in xml.getchildren():
# 			print_elem(children)
# 	else:
# 		a = '{0} -- {1}'.format(xml.tag.encode('utf-8'), xml.text.encode('utf-8') if xml.text else 'empty')
# 		print(a)

