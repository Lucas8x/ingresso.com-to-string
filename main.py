from datetime import datetime

import requests

from utils import write_to_txt


def get_session_type(session: dict) -> str:
  types = session['types']
  return ', '.join([type_i['alias'] for type_i in types])


class Formatter:
  def __init__(self, type_on_time: bool = False, type_on_room: bool = False, group_by_type: bool = False):
    self.type_on_time = type_on_time
    self.type_on_room = type_on_room
    self.group_by_type = group_by_type

  def session_to_string(self, session: dict) -> str:
    types_str = get_session_type(session)
    result = f'{session["time"]}'
    if self.type_on_time:
      result += f'[{types_str}]'
    return result

  def room_to_string(self, room: dict) -> str:
    sessions = room['sessions']
    sessions_arr = [self.session_to_string(session) for session in sessions]
    sessions_str = ' | '.join(sessions_arr)

    room_type = get_session_type(sessions[0])
    room_type_str = f' - [{room_type}]' if self.type_on_room else ''

    return f'  {room["name"]}{room_type_str}\n    {sessions_str}\n'

  def theater_to_string(self, theater: dict) -> str:
    rooms_str = ''
    for room in theater['rooms']:
      rooms_str += self.room_to_string(room)
    return f'{theater["name"]}\n{rooms_str}'


def main() -> None:
  try:
    year = datetime.today().year

    city_id = int(input('Enter city ID\n> '))
    movie_id = int(input('Enter movie ID\n> '))

    date = input(f'Enter date [MM-DD - ex: 12-31]\n> {year}-')
    date = f'{year}-{date}' if date else datetime.today().strftime('%Y-%m-%d')

    query = {
      "date": date
    }

    print(f'Fetching sessions for movie {movie_id} on {date}')
    api_url = f'https://api-content.ingresso.com/v0/sessions/city/{city_id}/event/{movie_id}'
    response = requests.get(api_url, params=query)
    if response.status_code == 404:
      print(f'No sessions on {date}')
      return
    data = response.json()[0]

    fmt = Formatter(type_on_room=True)

    result = f'Sessions for {movie_id} on {date}\n'
    for theater in data['theaters']:
      theater_string = fmt.theater_to_string(theater)
      result += f'{theater_string}\n'

    print(result)
    write_to_txt(result)

  except KeyboardInterrupt:
    quit()
  except Exception as e:
    print(e, e.__class__.__name__)


if __name__ == '__main__':
  main()
