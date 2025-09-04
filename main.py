from datetime import datetime, timedelta
import os
import pytz
import requests
import traceback
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from ics import Calendar, Event


class SUEventScraper:
    def __init__(self):
        self.su_eventpage_url = 'https://www.cambridgesu.co.uk/whatson/'
        self.events_list = []
    
    def scrape_current_events(self) -> list[Event]:
        """
        Scrape current events from the SU website and return them as a list of Event.
        """
        response = requests.get(self.su_eventpage_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # TODO: dynamically find the correct msl_eventlist div that is non-empty
        # right now, there are 2, the first one is the empty one 
        event_list = soup.find_all(class_='msl_eventlist')[-1]
        events = event_list.find_all(class_='event_item')

        events_list = []

        for event in events:
            try:
                e = self._get_event_details(event)
                if e:
                    events_list.append(e)

            except Exception:
                event_url = urljoin(self.su_eventpage_url, event.find('a')['href'])
                print(f"Error processing event | {event_url}: {traceback.format_exc()}")
                continue

        self.events_list = events_list

    def get_events(self) -> list[Event]:
        return self.events_list

    def generate_ics_calendar(self, output_dir="./outputs") -> Calendar:

        os.makedirs(output_dir, exist_ok=True)

        calendar = Calendar()
        for e in self.events_list:
            calendar.events.add(e)

        # save ics file to output dir
        with open(f"{output_dir}/su_events_caa_{datetime.now().strftime('%Y%m%d-%H%M%S')}.ics", "w") as f:
            f.writelines(calendar.serialize_iter())

        return calendar

    def _get_event_details(self, event) -> Event:
        """
        Extracts details for a single event and returns it as an ICS Event object.
        """
        event_id = event.find('a')['href']  # hopefully unique
        event_url = urljoin(self.su_eventpage_url, event.find('a')['href'])

        event_soup = BeautifulSoup(requests.get(event_url).text, 'html.parser')
        text_container = event_soup.find(class_="text-container")

        event_title = text_container.find('h1').text
        event_description = event_soup.find(class_="e-details-txt").text.strip()
        event_details = text_container.find_all(class_="event-details")

        details_dict = {
            "id": event_id,
            "title": event_title,
            "date": None,
            "time": None,
            "start_datetime": None,
            "end_datetime": None,
            "location": None,
            "organisation": None,
            "description": event_description
        }

        for event_detail in event_details:
            if event_detail.find(class_="fa-calendar"):
                details_dict["date"] = event_detail.text.strip()

            elif event_detail.find(class_="fa-clock-o"):
                details_dict["time"] = event_detail.text.strip()
                parsed_times = self._parse_event_datetime(details_dict)
                details_dict["start_datetime"] = parsed_times["start_time"]
                details_dict["end_datetime"] = parsed_times["end_time"]

            elif event_detail.find(class_="fa-map-marker"):
                details_dict["location"] = event_detail.text.strip()

            elif event_detail.find(class_="fa-sitemap"):
                details_dict["organisation"] = event_detail.text.strip()

            elif event_detail.find(class_="e-details-txt"):
                details_dict["description"] = event_detail.text.strip()

        # Build ICS Event
        e = Event()
        e.name = details_dict["title"]
        e.begin = details_dict["start_datetime"]
        e.end = details_dict["end_datetime"]
        e.location = details_dict["location"]
        e.organizer = details_dict["organisation"]
        e.description = details_dict["description"]

        print(details_dict)
        print("\n")

        return e

    def _parse_event_datetime(self, event: dict) -> dict:
        tz = pytz.timezone("Europe/London")

        # Parse date
        date_obj = datetime.strptime(event['date'], "%A %d %B %Y").date()

        # Parse times
        start_str, end_str = event['time'].replace(' ', '').split("-")

        if start_str.lower() == "noon":
            start_str = "12pm"
        if end_str.lower() == "noon":
            end_str = "12pm"

        start_dt = datetime.strptime(f"{date_obj} {start_str}", "%Y-%m-%d %I%p") \
            if ":" not in start_str else datetime.strptime(f"{date_obj} {start_str}", "%Y-%m-%d %I:%M%p")
        end_dt = datetime.strptime(f"{date_obj} {end_str}", "%Y-%m-%d %I%p") \
            if ":" not in end_str else datetime.strptime(f"{date_obj} {end_str}", "%Y-%m-%d %I:%M%p")

        # attach timezone
        start_dt = tz.localize(start_dt)
        end_dt = tz.localize(end_dt)

        # handle rollover
        if end_dt <= start_dt:
            end_dt = end_dt + timedelta(days=1)

        return {
            "start_time": start_dt.strftime("%Y-%m-%d %H:%M:%S%z"),
            "end_time": end_dt.strftime("%Y-%m-%d %H:%M:%S%z")
        }


if __name__ == '__main__':
    scraper = SUEventScraper()
    scraper.scrape_current_events()
    print(scraper.get_events())
    scraper.generate_ics_calendar()