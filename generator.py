if __name__ == '__main__':
    with open("file.txt", "w") as file:

        for i in range(1, 101):
            file.write(f"""
  device{i}:
    build: device/
    command: python ./main.py {i}
    depends_on:
      - server
"""

                       )
