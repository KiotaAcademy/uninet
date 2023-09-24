# UjuziHub API Endpoints

The following API endpoints are available:

## Accounts App

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

## Notes App

### Categories

- **Create Categories in Bulk**: Create multiple categories at once.
  - Method: POST
  - URL: `http://localhost:8000/notes/categories/bulk_create/`
  - Request Data Example:
    ```json
    [
        {
            "name": "Mathematics"
        },
        {
            "name": "Music"
        },
        {
            "name": "Engineering"
        }
    ]
    ```

- **Create Single Category**: Create a single category.
  - Method: POST
  - URL: `http://localhost:8000/notes/categories/create/`
  - Request Data Example:
    ```json
    {
        "name": "Business"
    }
    ```

- **Get Categories**: Retrieve a list of all categories.
  - Method: GET
  - URL: `http://localhost:8000/notes/categories/`

- **Delete Category by ID**: Delete a category by its ID.
  - Method: DELETE
  - URL: `http://localhost:8000/notes/categories/<category_id>/`

- **Delete Category by Name**: Delete a category by its name.
  - Method: DELETE
  - URL: `http://localhost:8000/notes/categories/delete_by_name/<category_name>/`

- **Delete Categories in Bulk**: Delete multiple categories at once.
  - Method: DELETE
  - URL: `http://localhost:8000/notes/categories/bulk_delete/`
  - Request Data Example:
    ```json
    {
        "category_names": ["Mathematics", "Music", "Engineering"]
    }
    ```

### Documents

- **Upload Document**: Upload a document.
  - Method: POST
  - URL: `http://localhost:8000/notes/documents/`
  - Request Data Example:
    ```json
    {
        "documents": <file>,
        "categories": [1, 2],  // Optional
        "title": "Document Title"  // Optional
    }
    ```
  - Note: Authentication details are required in the header.
    - Key: Authorization
    - Value: Token <your_auth_token>

- **Download Document by ID**: Download a document by its ID.
  - Method: GET
  - URL: `http://localhost:8000/notes/documents/<document_id>/download_document_by_id/`
  - Note: Authentication details are required in the header.
    - Key: Authorization
    - Value: Token <your_auth_token>

- **Download Document by Title**: Download a document by its title.
  - Method: GET
  - URL: `http://localhost:8000/notes/documents/<document_title>/download_document_by_title/`
  - Note: Authentication details are required in the header.
    - Key: Authorization
    - Value: Token <your_auth_token>

- **Download URLs for All Documents**: Get download URLs for all documents.
  - Method: GET
  - URL: `http://localhost:8000/notes/documents/document_urls/`
  - Note: Authentication details are required in the header.
    - Key: Authorization
    - Value: Token <your_auth_token>

- **Download URLs by Document IDs**: Get download URLs by providing document IDs in the query.
  - Method: GET
  - URL: `http://localhost:8000/notes/documents/document_urls/?ids=<document_id_1>,<document_id_2>`
  - Note: Authentication details are required in the header.
    - Key: Authorization
    - Value: Token <your_auth_token>

- **Download URLs by Document Titles**: Get download URLs by providing document titles in the query.
  - Method: GET
  - URL: `http://localhost:8000/notes/documents/document_urls/?titles=<document_title_1>,<document_title_2>`
  - Note: Authentication details are required in the header.
    - Key: Authorization
    - Value: Token <your_auth_token>

### Topics

- **Create Topic**: Create a new topic.
  - Method: POST
  - URL: `http://localhost:8000/notes/topics/create_topic/`
  - Request Data Example:
    - Form Data:
      - Keys: `document_title` (optional), `start_page` (optional), `end_page` (optional), `uploaded_document` (file)
    - Note: Either `document_title` or `uploaded_document` must be provided. If both are provided, a document is created with the provided title and the topic is associated with that document. If only one is provided, the code attempts to find an existing document or create a new one.
    
    - Note: Authentication details are required in the header.
      - Key: Authorization
      - Value: Token <your_auth_token>

- **Get All Topics**: Retrieve a list of all topics.
  - Method: GET
  - URL: `http://localhost:8000/notes/topics/`

- **Get Topic by ID**: Retrieve a topic by its ID.
  - Method: GET
  - URL: `http://localhost:8000/notes/topics/<topic_id>/`

- **Get Topics by Name**: Retrieve topics by name.
  - Method: GET
  - URL: `http://localhost:8000/notes/topics/<topic_name>/`

- **Update Topic**: Update a topic by providing parameters in the query.
  - Method: PUT
  - URL: `http://localhost:8000/notes/topics/update_topic/?topic_name=<topic_name>&document_title=<document_title>`
  - Request Data Example (Form Data): Fields to be updated.
    - Note: Parameters are provided in the query.
    

- **Delete Topic**: Delete a topic by providing parameters in the query.
  - Method: DELETE
  - URL: `http://localhost:8000/notes/topics/delete_topic/?topic_name=<topic_name>&document_title=<document_title>`
  - Note: Parameters are provided in the query.
    

### Lectures

- **Create Lecture**: Create a new lecture.
  - Method: POST
  - URL: `http://localhost:8000/notes/lectures/create_lecture/`
  - Request Data Example:
    ```json
    {
        "lecturer": 3,
        "name": "jazzcvdddfff",
        "description": "symphony of the opera",
        "students": [2, 3],
        "topics": [1, 9]
    }
    ```
  

- **Get All Lectures**: Retrieve a list of all lectures.
  - Method: GET
  - URL: `http://localhost:8000/notes/lectures/`

- **Get Lecture by ID**: Retrieve a lecture by its ID.
  - Method: GET
  - URL: `http://localhost:8000/notes/lectures/<lecture_id>/`

- **Update Lecture by ID**: Update a lecture by its ID.
  - Method: PUT
  - URL: `http://localhost:8000/notes/lectures/update_lecture/`
  - Request Data Example:
    ```json
    {
        "id": 21,
        "topics": [1, 9]
    }
    ```
  

- **Update Lecture by Query Parameters**: Update a lecture by providing its ID in query parameters.
  - Method: PUT
  - URL: `http://localhost:8000/notes/lectures/update_lecture/?id=<lecture_id>`
 

- **Delete Lecture by Query Parameters**: Delete a lecture by providing its ID in query parameters.
  - Method: DELETE
  - URL: `http://localhost:8000/notes/lectures/delete_lecture/?id=<lecture_id>`
 

- **Delete Lecture by Request Data**: Delete a lecture by providing its ID in request data.
  - Method: DELETE
  - URL: `http://localhost:8000/notes/lectures/delete_lecture/`
  - Request Data Example:
    ```json
    {
        "id": 25
    }
    ```
 







## Testing API endpoints

To interact with the API endpoints for your newly created project, you can use tools like [Postman](https://www.postman.com/) to send HTTP requests to the API endpoints. Here's how you can use Postman:

1. Install Postman on your machine from the [Postman website](https://www.postman.com/downloads/).
2. Launch Postman and create a new request.
3. Set the request method (e.g., POST, GET) and URL for the desired API endpoint.
4. Add any required headers or request parameters.
5. Send the request and view the response.


Make sure to replace `http://localhost:8000/` in the API URL with the appropriate base URL if running the API on a different host or port.