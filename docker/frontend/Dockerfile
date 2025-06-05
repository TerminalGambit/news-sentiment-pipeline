FROM node:18-alpine

WORKDIR /app

# Install dependencies
COPY frontend/package*.json ./
RUN npm install

# Copy the rest of the application
COPY frontend .

# Build the application
RUN npm run build

# Install serve to run the application
RUN npm install -g serve

# Expose the port
EXPOSE 3000

# Start the application
CMD ["serve", "-s", "build", "-l", "3000"] 