# introduction

Sample authentication app using [FastAPI](https://fastapi.tiangolo.com/) and [PostgreSQL](https://www.postgresql.org/).

## requirements

- [Docker](https://www.docker.com/)
- [Python 3.10+](https://www.python.org/)
- postgres table creation

    ```sql
    CREATE TABLE public.users (
    user_id UUID NOT NULL,
    email VARCHAR(100) NOT NULL,
    password BYTES NOT NULL,
    created TIMESTAMP NOT NULL,
    "role" VARCHAR(25) NOT NULL,
    CONSTRAINT users_pkey PRIMARY KEY (user_id ASC),
    UNIQUE INDEX email_comp_idx (email ASC) STORING (password, "role", created)
    )
    ```

## endpoints

- `/api/v1/login`
- `/api/v1/register`

```json
# sample request body
{
    "email": "testing@gmail.com",
    "password": "testing123"
}
```
