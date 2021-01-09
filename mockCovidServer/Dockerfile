FROM node:12
WORKDIR /app/mockCovidServer
COPY . .
EXPOSE 3000
RUN npm install -g json-server
#RUN ls
#CMD json-server mockCovidServer/db.json
CMD ["json-server", "-H", "0.0.0.0", "mockCovidServer/db.json"]