import time

def victimLoop():
  while True:
    print('Torturing...')
    time.sleep(3)

if __name__ == '__main__':
  try:
    victimLoop()
  except KeyboardInterrupt:
    print('\nAgent exited')
  except Exception as e:
    print(e)