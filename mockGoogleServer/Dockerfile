FROM node:12
WORKDIR /app/mockGoogleServer
COPY . .
EXPOSE 3000
RUN npm install -g json-server
#RUN ls
#CMD json-server mockGoogleServer/db.json
CMD ["json-server", "-H", "0.0.0.0", "mockGoogleServer/db.json"]