## Cloud based e-commerce REST API
* At university, i have got this final project to build a e-commerce backend API built with **Fast api**. This application implements a simple product catalog and secure order processing system. 

##  Key Architectural Features

* 1. Business logic is decoupled from the routing controllers via a dedicated service Layer (`ProductService`), keeping endpoints lightweight and maintainable.
* 2. I created a resource protection using OAuth2 password and **JWT (JSON Web Tokens)** containing short-lived expiration vectors (HS256).
* 3. Custom HTTP middleware logs every transaction (HTTP Method, Route Path, Status Code, and Request Duration) to a dedicated `api_access.log` engine.
* 4. Used **Pydantic** schema models to execute strict input serialization and request type validation.
* 5. Explicit error boundaries translating architectural anomalies into native HTTP exceptions with semantic status codes.

##  Tech Stack & Dependencies

*   **Core Framework:** FastAPI (Python)
*   **ASGI Server:** Uvicorn
*   **Security & Encryption:** Jose (JWT Handling), Passlib (BCrypt Hashing)
*   **Validation Engine:** Pydantic

 ##  API Specification & Endpoints

 ### Public Endpoints
*   `GET /` - **Health Check:** Returns API engine status and cloud availability configuration.
*   `GET /products` - **Product Catalog:** retrieves list of available products.

 ### Security Endpoints
*   `POST /login` - **Authentication Broker:** Accepts payload credentials and creates valid Bearer Access Tokens.

 ### Protected Endpoints 
*   `POST /orders` - **Place Order:** Processes checkout logic against the catalog service tier.
