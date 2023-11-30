import time

def agentLoop():
  while True:
    print('Running')
    time.sleep(3)

if __name__ == '__main__':
  try:
    agentLoop()
  except KeyboardInterrupt:
    print('\nAgent exited')
  except Exception as e:
    print(e)