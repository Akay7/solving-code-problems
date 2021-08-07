# Solving Code Problems (API)

## How to run project

1. You should have installed docker and docker-compose

2. Run project

    ```docker-compose -f docker-compose.yml -f docker-compose.dev.yml up --build```

3. Migrate database

    ```docker-compose exec scp_backend /bin/bash -c "python3 manage.py migrate"```

4. Run tests(optional)

    ```docker-compose exec scp_backend /bin/bash -c "pytest"```

5. Create superuser

   ```docker-compose exec scp_backend /bin/bash -c "python3 manage.py createsuperuser"```