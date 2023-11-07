# autoed
Automatic Marking of UML Database Questions Education System

## How to work on frontend (dev)
1. cd into frontend_student
2. ``npm install`` (make sure node modules is deleted)
3. ``npm run dev`` 
4. Start coding and go to localhost:3000/editor

## How to work on backend (dev)
1. cd into backend
2. create superuser by doing the command  ``docker-compose -f local.yml run --rm django python manage.py createsuperuser ``
3. start dev by running ``docker-compose -f local.yml up``