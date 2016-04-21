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


class CollectorTarget(object):
    def __init__(self):
        self.events = []

    def start(self, tag, attrib):
        self.events.append("start %s %r" % (tag, dict(attrib)))

    def end(self, tag):
        self.events.append("end %s" % tag)

    def data(self, data):
        self.events.append("data %r" % data)

    def comment(self, text):
        self.events.append("comment %s" % text)

    def close(self):
        self.events.append("close")
        return "closed!"


def recursive_parser(xml_root):
    result_dict = dict()
    for id,  child in enumerate(xml_root.getchildren()):
        tmp_dict = dict()
        attrib_dict = dict()
        r_dict = dict()
        use_attrib = True
        res = ''
        if child.attrib:
            for key, value in child.attrib.items():
                attrib_dict[key] = value
        if child.getchildren():
            tmp_dict = recursive_parser(child)
        else:
            if child.getparent().tag not in ['events', 'event']:
                for current_tag in child.getparent().getchildren():
                    if current_tag.text:
                        res += current_tag.text
                        res += '; '
            else:
                res = child.text
            if not res and attrib_dict:
                res = [value for value in attrib_dict.values()]
                use_attrib = False
            if use_attrib:
                r_dict['attrib'] = attrib_dict

        r_dict[child.tag] = tmp_dict if tmp_dict else res
        result_dict[id] = r_dict
    return result_dict


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

    # if sys.version_info.major == 3:
    #     xml = etree.fromstring(xml_text.encode('utf-8'))
    # else:
    #     xml = etree.fromstring(xml_text)

    # events = xml.find('events')
    # places = xml.find('places')
    # schedule = xml.find('schedule')

    # a = recursive_parser(events)
    # for i, j in a.items():
    #     print('{0} - {1}\n'.format(i, j))
    # get_events(events)
    # get_places(places)
    # get_schedule(schedule)

    custom_parser = etree.XMLParser(target=CollectorTarget())
    result = etree.XML(xml_text, custom_parser)

    return result, custom_parser
    # return 'the creation of records in the database successfully'


class CustomParser(object):
    def __init__(self):
        xml_text = self.get_rss(current_dir)
        if sys.version_info.major == 3:
            xml = etree.fromstring(xml_text.encode('utf-8'))
        else:
            xml = etree.fromstring(xml_text)
        self.xml = etree.fromstring(xml)

    def get_rss(self, directory):
        file = open('{0}/test.xml'.format(directory))
        file_text = file.read()
        file.close()
        return file_text

    def get_children_dict(self, element):
        return {child.gat: child.getchildren() for child in element.getchildren()}

    def get_parent_dict(self):
        return self.get_children_dict(self.xml)

    def parse(self):
        parent_elements = self.get_parent_dict()
        for parent in parent_elements:
            self.parse_element(parent)

    def parse_element(self, element):
        elements = self.get_children_dict(element)
        for elem in elements:
            tmp_dict = dict()
            if elem.attrib:
                tmp_dict = elem.attrib
            if elem.get_children():
                tmp_dict[elem.tag] = '; '.join([child.tag for child in elem.get_children])

            
