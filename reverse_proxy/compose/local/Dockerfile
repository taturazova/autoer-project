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