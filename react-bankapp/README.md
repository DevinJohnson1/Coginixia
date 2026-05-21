# Coginixia Bank Frontend

This React app is a basic operations dashboard for your Python FastAPI backend.

## What It Supports

- Configure backend `Base URL` and required path secret (`API_PATH_SECRET` value)
- Register new users with a required shared register token (`REGISTER_TOKEN`)
- List all customers
- List premium customers (`balance > 10000`)
- Filter customers by minimum balance
- Fetch a customer by ID
- Create customers
- Update existing customers
- Delete customers

## Backend Endpoint Pattern

The frontend calls your backend using this pattern:

`/api/{api_secret}/customers`

Examples used in the UI:

- `GET /api/{api_secret}/customers`
- `GET /api/{api_secret}/customers/premium`
- `GET /api/{api_secret}/customers/balance/min/{balance}`
- `GET /api/{api_secret}/customers/{id}`
- `POST /api/{api_secret}/customers`
- `PUT /api/{api_secret}/customers/{id}`
- `DELETE /api/{api_secret}/customers/{id}`

## Run Locally

1. Start your backend (default expected at `http://localhost:8000`).
2. In this folder, install dependencies:

```bash
npm install
```

3. Start the frontend:

```bash
npm run dev
```

4. Open the shown Vite URL (usually `http://localhost:5173`).
5. Enter:
	- Base URL: `http://localhost:8000`
	- API Path Secret: your backend `API_PATH_SECRET` value

## Notes

- If requests fail from the browser due to CORS, add FastAPI CORS middleware or serve frontend/backend under the same origin.
- Production build command:

```bash
npm run build
```

- Run frontend tests:

```bash
npm run test
```

