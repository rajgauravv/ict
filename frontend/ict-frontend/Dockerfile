FROM node:14

# set the working directory in container
WORKDIR /app

# copy the package.json and package-lock.json files into the container
COPY package*.json ./

# installin Node.js dependencies
RUN npm install

# coy the application's source code to the container
COPY . .

# Expose the port
EXPOSE 3000

# Starting React application
CMD ["npm", "start"]
