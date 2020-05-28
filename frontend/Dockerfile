FROM node:12-stretch as build
WORKDIR /usr/app
COPY package.json .
RUN yarn install
COPY . .
RUN yarn build

FROM nginx:alpine as production
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
COPY --from=build /usr/app/build /usr/share/nginx/html

