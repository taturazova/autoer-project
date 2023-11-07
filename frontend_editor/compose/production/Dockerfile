FROM node:16-alpine as build

# Set the working directory in the docker container
# This is equivalent in Linux commands to: mkdir -p /app && cd app
WORKDIR /app

# add `/app/node_modules/.bin` to the $PATH
# This ensures all NPM utilites we install have their CLIs
# available on the command line
ENV PATH /app/node_modules/.bin:$PATH

# Install all react app dependencies
COPY package.json ./
COPY package-lock.json ./
RUN npm ci
RUN npm install react-scripts@4.0.3 -g

# Copy project into the container and build
COPY . ./
RUN npm run build

# Host production react instance using Nginx
FROM nginx:stable-alpine

# Copy build react app to nginx for hosting
COPY --from=build /app/build /usr/share/nginx/html
# To enable react router, we need to specially configure
# Nginx to enable proper routing
COPY ./nginx/nginx.conf /etc/nginx/conf.d/default.conf

# Start Nginx
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]