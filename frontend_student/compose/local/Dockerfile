FROM node:16-alpine

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
# npm install --silent can be substituted here to silence
# the installation procedure (which can be CLI intensive), however,
# this also silences any error output.
RUN npm install
# Install globally for the ability to run npm runner commands
# specific to react
RUN npm install react-scripts@4.0.3 -g

# Copy the contents of the app's directory to the container
COPY . ./

# Start the react app
CMD ["npm", "start"]