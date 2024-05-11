if __name__ == '__main__':
    with open("file.txt", "w") as file:

        for i in range(1, 101):
            file.write(f"""
  device{i}:
    build: device/
    command: python ./main.py {i} {8080 + (i * 3)}
    depends_on:
      - server
    ports:
      - "{8080 + (i * 3)}-{8080 + (i * 3) + 2}:{8080 + (i * 3)}-{8080 + (i * 3) + 2}"
"""

                       )
