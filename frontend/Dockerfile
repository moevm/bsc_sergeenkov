FROM node:stretch as build
WORKDIR /usr/app
COPY package.json .
RUN yarn install
ARG ARG_REACT_APP_ENV
ARG ARG_REACT_APP_SENTRY_DSN
ARG ARG_REACT_APP_BASE_URL
ENV REACT_APP_ENV=$ARG_REACT_APP_ENV
ENV REACT_APP_SENTRY_DSN=$ARG_REACT_APP_SENTRY_DSN
ENV REACT_APP_BASE_URL=$ARG_REACT_APP_BASE_URL
COPY . .
RUN yarn build

FROM nginx:alpine as production
RUN apk add curl
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
COPY --from=build /usr/app/build /usr/share/nginx/html

