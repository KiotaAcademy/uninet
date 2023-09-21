# UjuziHub 
## API Endpoints
The following API endpoints are available:

- **User Registration**: Register a new user.
  - Method: POST
  - URL: `http://localhost:8000/accounts/register/`
  - Fields: `username`, `email`, `password`

- **Verify Email**: Verify the user's email address using the verification token received via email.
  - Method: GET
  - URL: `http://localhost:8000/accounts/verify-email/`
  - Requires authentication: No
  
- **User Login**: Log in a user and obtain an authentication token.
  - Method: POST
  - URL: `http://localhost:8000/accounts/login/`
  - Fields: `username`, `password`

- **User Logout**: Log out the authenticated user.
  - Method: POST
  - URL: `http://localhost:8000/accounts/logout/`
  - Requires authentication: Yes
  
- **Get User Profile**: Get the profile information of the authenticated user.
  - Method: GET
  - URL: `http://localhost:8000/accounts/profile/`
  - Requires authentication: Yes

- **Update User Profile**: Update the profile information of the authenticated user.
  - Method: POST
  - URL: `http://localhost:8000/accounts/profile/`
  - Requires authentication: Yes


- **Delete User**: Delete the authenticated user's account.
  - Method: DELETE
  - URL: `http://localhost:8000/accounts/delete/`
  - Requires authentication: Yes
  
## Testing API endpoints

To interact with the API endpoints for your newly created project, you can use tools like [Postman](https://www.postman.com/) to send HTTP requests to the API endpoints. Here's how you can use Postman:

1. Install Postman on your machine from the [Postman website](https://www.postman.com/downloads/).
2. Launch Postman and create a new request.
3. Set the request method (e.g., POST, GET) and URL for the desired API endpoint.
4. Add any required headers or request parameters.
5. Send the request and view the response.


Make sure to replace `http://localhost:8000/` in the API URL with the appropriate base URL if running the API on a different host or port.