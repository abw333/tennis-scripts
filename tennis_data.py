if __name__ == '__main__':
  import sys

  if len(sys.argv) < 2:
    print('Missing command.')
    exit()

  command = sys.argv[1]
  if command == 'download':
    import os
    import shutil
    import urllib.request

    zipped_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tennis-data', 'zipped')

    if os.path.exists(zipped_dir):
      shutil.rmtree(zipped_dir)

    os.makedirs(zipped_dir)

    for year in range(2000, 2020):
      file_name = f'{year}.zip'

      print(f'Downloading {file_name}', end='\r')

      urllib.request.urlretrieve(
        f'http://www.tennis-data.co.uk/{year}/{file_name}',
        os.path.join(zipped_dir, file_name)
      )
  else:
    print(f'Invalid command: {command}')
