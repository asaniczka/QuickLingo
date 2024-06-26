# Use the official Nginx base image
FROM nginx:latest

# Copy custom Nginx configuration file
COPY nginx.conf /etc/nginx/nginx.conf

# Expose port 80
EXPOSE 80

# Start Nginx service
CMD ["nginx", "-g", "daemon off;"]
