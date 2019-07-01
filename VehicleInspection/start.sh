gunicorn VehicleInspection.wsgi:application -c gunicorn.conf > ./gunicorn.log 2>&1 &
