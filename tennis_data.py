if __name__ == '__main__':
  import os
  import shutil
  import sys

  if len(sys.argv) < 2:
    print('Missing command.')
    exit()

  tennis_data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tennis-data')
  zipped_dir = os.path.join(tennis_data_dir, 'zipped')
  unzipped_dir = os.path.join(tennis_data_dir, 'unzipped')
  csv_dir = os.path.join(tennis_data_dir, 'csv')

  command = sys.argv[1]
  if command == 'download':
    import urllib.request

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
  elif command == 'unzip':
    import zipfile

    if not os.path.exists(zipped_dir):
      print('Must download data before unzipping it.')
      exit()

    if os.path.exists(unzipped_dir):
      shutil.rmtree(unzipped_dir)

    os.makedirs(unzipped_dir)

    for file_name in sorted(os.listdir(zipped_dir)):
      print(f'Unzipping {file_name}', end='\r')

      with zipfile.ZipFile(os.path.join(zipped_dir, file_name)) as z:
        z.extractall(unzipped_dir)
  elif command == 'csv':
    import csv
    import xlrd

    if not os.path.exists(unzipped_dir):
      print('Must unzip data before converting it to CSV.')
      exit()

    if os.path.exists(csv_dir):
      shutil.rmtree(csv_dir)

    os.makedirs(csv_dir)

    for file_name in sorted(os.listdir(unzipped_dir)):
      print(f'Converting {file_name} to CSV', end='\r')

      sheet = xlrd.open_workbook(os.path.join(unzipped_dir, file_name)).sheet_by_index(0)

      data = tuple(tuple(cell.value for cell in row) for row in sheet.get_rows())

      with open(os.path.join(csv_dir, os.path.splitext(file_name)[0] + '.csv'), 'w') as f:
        csv.writer(f).writerows(data)
  else:
    print(f'Invalid command: {command}')
