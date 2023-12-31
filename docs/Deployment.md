# Production Deployment

The following instructions represent a general outline for deploying AutoEd to a given server. The following process is generally hosting agnostic, however, the OS is assumed to be Linux-based.

1. Clone AutoEd to an appropriate directory on the server. The location of this directory is up to the user, however, this directory should be readable and writeable by Docker.

2. Define the appropriate environment variables for use in Postgres and Django. These can either be defined inside environment files or as environment variables. The environment files for Django and Postgres follow (relative to the project root):

    Django Environment File: `/backend/.envs/.production/.django`

    Postgres Environment File: `/backend/.envs/.production/.postgres`

    The follow environment variables must be defined within each for a successful deployment:

    Django Environment Variables
    ```bash
    USE_DOCKER=yes
    IPYTHONDIR=/app/.ipython
    # The Django Secret Key must be generated by the user. This key can be any random, lengthy string (recommended minimum of 16 chars).
    DJANGO_SECRET_KEY=GENERATED_KEY_GOES_HERE
    DJANGO_SETTINGS_MODULE=config.settings.production
    # The Docker URL of the Redis server used for caching with Django
    REDIS_URL=http://redis:6379
    # The desired location of the Django Admin panel
    DJANGO_ADMIN_URL=https://autoed.ok.ubc.ca/admin
    # A single value or list of acceptable hosts that the Django app can be accessed from
    DJANGO_ALLOWED_HOSTS=autoed.ok.ubc.ca
    ```

    Postgres Environment Variables:
    ```bash
    # The host and post of the database. Should be left as default unless changed explicitly in the codebase.
    POSTGRES_HOST=postgres
    POSTGRES_PORT=5432
    # The name of the database used within postgres
    POSTGRES_DB=auto_marking_api
    # The username and password used by Postgres to access and read/write to the database. These values should be randomly generated and kept secret.
    POSTGRES_USER=GENERATED_USERNAME_GOES_HERE
    POSTGRES_PASSWORD=GENERATED_KEY_GOES_HERE
    ```

3. Change any settings necessary to ensure the Django app hosts from the /app subfolder and the Student app serves from the site root.

4. With the above configuration in place, the AutoEd system can be deployed through use of `docker-compose` (run at the project's root) as follows:

    To deploy AutoEd as an attached process:
    ```bash
    docker-compose -f production.yml up
    ```

    To deploy AutoEd as an unattached process:
    ```bash
    docker-compose -f production.yml up -d
    ```

5. To shutdown a deploy instance of AutoEd, run the following at the project root:

    ```
    docker-compose -f 'production.yml' down
    ```