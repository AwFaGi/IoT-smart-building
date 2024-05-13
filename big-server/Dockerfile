FROM maven:3.9.6-eclipse-temurin-17-focal
WORKDIR /big-server/
COPY . .

RUN mvn -DskipTests package
