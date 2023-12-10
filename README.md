# Table of Contents
- [Table of Contents](#table-of-contents)
- [UjuziHub API Endpoints](#ujuzihub-api-endpoints)
  - [Accounts App](#accounts-app)
  - [Institutions App](#institutions-app)
    - [Institution](#institution)
      - [Create Institution](#create-institution)
      - [Get Institution](#get-institution)
      - [Update Institution](#update-institution)
    - [School](#school)
      - [Create School](#create-school)
      - [Get School](#get-school)
      - [Update School](#update-school)
      - [Delete School](#delete-school)
    - [Department](#department)
      - [Create Department](#create-department)
      - [Get Department](#get-department)
      - [Update Department](#update-department)
      - [Delete Department](#delete-department)
    - [Course](#course)
      - [Create Course](#create-course)
      - [Get Course](#get-course)
      - [Update Course](#update-course)
      - [Delete Course](#delete-course)
    - [Unit](#unit)
      - [Create Unit](#create-unit)
      - [Get Unit](#get-unit)
      - [Update Unit](#update-unit)
      - [Delete Unit](#delete-unit)
  - [Clubs and Societies App](#clubs-and-societies-app)
    - [ClubSociety](#clubsociety)
      - [Create Club/Society](#create-clubsociety)
      - [Get Club/Society](#get-clubsociety)
      - [Update Club/Society](#update-clubsociety)
      - [Delete Club/Society](#delete-clubsociety)
  - [Lecturers App](#lecturers-app)
    - [Lecturer](#lecturer)
      - [Create Lecturer](#create-lecturer)
      - [Get Lecturer](#get-lecturer)
      - [Update Lecturer](#update-lecturer)
      - [Delete Lecturer](#delete-lecturer)
  - [Notes App](#notes-app)
    - [Categories](#categories)
      - [Create Categories in Bulk](#create-categories-in-bulk)
      - [Create Single Category](#create-single-category)
      - [Get Categories](#get-categories)
      - [Delete Category by ID](#delete-category-by-id)
      - [Delete Category by Name](#delete-category-by-name)
      - [Delete Categories in Bulk](#delete-categories-in-bulk)
    - [Documents](#documents)
      - [Upload Document](#upload-document)
      - [Download Document by ID](#download-document-by-id)
      - [Download Document by Title](#download-document-by-title)
      - [Download URLs for All Documents](#download-urls-for-all-documents)
      - [Download URLs by Document IDs](#download-urls-by-document-ids)
      - [Download URLs by Document Titles](#download-urls-by-document-titles)
    - [Topics](#topics)
      - [Create Topic](#create-topic)
      - [Get All Topics](#get-all-topics)
      - [Get Topic by ID](#get-topic-by-id)
      - [Get Topics by Name](#get-topics-by-name)
      - [Update Topic](#update-topic)
      - [Delete Topic](#delete-topic)
    - [Lectures](#lectures)
      - [Create Lecture](#create-lecture)
      - [Get All Lectures](#get-all-lectures)
      - [Get Lecture by ID](#get-lecture-by-id)
      - [Update Lecture by ID](#update-lecture-by-id)
      - [Update Lecture by Query Parameters](#update-lecture-by-query-parameters)
  - [Testing API endpoints](#testing-api-endpoints)

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




## Institutions App
### Institution

#### Create Institution
- Method: POST
- URL: `http://localhost:8000/institutions/institution/`
- Requires authentication: Yes
- Headers:
  - Key: Authorization
  - Value: Token <your_auth_token>
- Request Data Example:
    ```json
    {
        "category": "university",
        "name": "<institution_name>"
    }
    ```
- Sample Response:
    ```json
    {
        "id": 73,
        "chancellor": "<chancellor_username>",
        "vice_chancellor": null,
        "admins": ["<chancellor_username>", "<created_by_username>", "<admin1_username>", "<admin2_username>"],
        "created_by": "<created_by_username>",
        "category": "university",
        "name": "<institution_name>"
    }
    ```
- `Note:` Chancellor, vice_chancellor, and created_by are always added by default to the admins list. Their admin status cannot be changed unless new users are provided in their place, i.e., if the chancellor is changed to a different user.

#### Get Institution
- Method: GET
- URL: `http://localhost:8000/institutions/institution/retrieve_institution/?name=<institution_name>`
- `NOTE:` You can also provide the primary key or id of the institution alone instead of providing the name. Provide it for the key 'id'.
- Requires authentication: Yes
- Headers:
  - Key: Authorization
  - Value: Token <your_auth_token>
- Sample Response:
    ```json
    {
        "id": 73,
        "chancellor": "<chancellor_username>",
        "vice_chancellor": null,
        "admins": ["<chancellor_username>", "<created_by_username>", "<admin1_username>", "<admin2_username>"],
        "created_by": "<created_by_username>",
        "category": "university",
        "name": "<institution_name>"
    }
    ```

#### Update Institution
- Method: PUT
- URL: `http://localhost:8000/institutions/institution/update_institution/?name=<institution_name>`
- `NOTE:` You can also provide the primary key or id of the institution alone instead of providing the name. Provide it for the key 'id'.
- Requires authentication: Yes
- Headers:
  - Key: Authorization
  - Value: Token <your_auth_token>
- Sample Request Data:
    ```json
    {
        "chancellor": "<new_chancellor_username>",
        "remove_admins": ["<admin1_username>"]
    }
    ```
- Sample Response: Updated institution details.
    ```json
    {
        "id": 73,
        "chancellor": "<new_chancellor_username>",
        "vice_chancellor": null,
        "admins": ["<chancellor_username>", "<created_by_username>", "<admin2_username>"],
        "created_by": "<created_by_username>",
        "category": "university",
        "name": "<institution_name>"
    }
    ```
- **Response when not authorized:**
  ```json
  {
      "error": "You are not authorized to update this institution. Only institution-level admins can update."
  }

#### Delete Institution
- Method: DELETE
- URL: `http://localhost:8000/institutions/institution/delete_institution/?name=<institution_name>`
- `NOTE:` You can also provide the primary key or id of the institution alone instead of providing the name. Provide it for the key 'id'.
- Requires authentication: Yes
- Headers:
  - Key: Authorization
  - Value: Token <your_auth_token>
- Sample Response: Message indicating successful deletion.
- **Response when not authorized:**
 ```json
 {
    "error": "You are not authorized to DELETE this institution. Only institution-level admins can DELETE."
}
```



### School

#### Create School
- Method: POST
- URL: `http://localhost:8000/institutions/school/`
- Requires authentication: Yes
- Headers:
  - Key: Authorization
  - Value: Token <your_auth_token>
- Request Data Example:
    ```json
    {
        "name": "<school_name>",
        "head": "<head_username>",
        "admins": ["<school_admin1_username>", "<school_admin2_username>"]
    }
    ```
- Sample Response:
    ```json
    {
        "id": <school_id>,
        "name": "<school_name>",
        "head": "<head_username>",
        "admins": ["<head_username>", "<school_admin1_username>", "<school_admin2_username>", "created_by_username"],
        "created_by": "<created_by_username>",
        "institution": "<institution_name>"
    }
    ```
- `Note:` The institution is automatically set based on the institution the user is an admin. If not an institution-level admin in any institution, the user can't create schools.

#### Get School
- Method: GET
- URL: `http://localhost:8000/institutions/school/retrieve_school/?name=<school_name>&institution=<institution_name>`
- `NOTE:` You can also provide the primary key or id of the school alone instead of providing name and institution. Provide it for the key 'id'.
- Requires authentication: Yes
- Headers:
  - Key: Authorization
  - Value: Token <your_auth_token>
- Sample Response:
    ```json
    {
        "id": <school_id>,
        "name": "<school_name>",
        "head": "<head_username>",
        "admins": ["<head_username>", "<school_admin1_username>", "<school_admin2_username>", "created_by_username"],
        "created_by": "<created_by_username>",
        "institution": "<institution_name>"
    }
    ```
- **Response when no parameters provided:**
    ```json
    {
        "error": "You must provide either the 'id' or 'name' parameter for the lookup."
    }
- **Response when no institution provided: All schools with that name are returned**
    ```json
    [
        {
            "id": <school_id_1>,
            "name": "<school_name>",
            "head": "<head_username>",
            "admins": ["<head_username>", "<school_admin1_username>", "<school_admin2_username>", "created_by_username"],
            "created_by": "<created_by_username>",
            "institution": "<institution_name_1>"
        },
        {
            "id": <school_id_2>,
            "name": "<school_name>",
            "head": "<head_username>",
            "admins": ["<head_username>", "<school_admin1_username>", "<school_admin2_username>", "created_by_username"],
            "created_by": "<created_by_username>",
            "institution": "<institution_name_2>"
        },
        
    ]
    ```

#### Update School
- Method: PUT
- URL: `http://localhost:8000/institutions/school/update_school/?name=<school_name>&institution=<institution_name>`
- `NOTE:` You can also provide the primary key or id of the school alone instead of providing name and institution. Provide it for the key 'id'.
- Requires authentication: Yes
- Headers:
  - Key: Authorization
  - Value: Token <your_auth_token>
- Sample Request Data:
    ```json
    {
        "head": "<new_head_username>",
        "remove_admins": ["<school_admin1_username>"],
        "admins":["<school_admin3_username>"]
    }
    ```
- Sample Response: Updated school details.
    ```json
    {
        "id": <school_id>,
        "name": "<school_name>",
        "head": "<head_username>",
        "admins": ["<new_head_username>", "<school_admin2_username>", "<school_admin3_username>", "created_by_username"],
        "created_by": "<created_by_username>",
        "institution": "<institution_name>"
    }
    ```
- **Response when not authorized:**
    ```json
    {
        "error": "You are not authorized to update this school. Only school-level admins can update."
    }

#### Delete School
- Method: DELETE
- URL: `http://localhost:8000/institutions/school/delete_school/?name=<school_name>&institution=<institution_name>`
- `NOTE:` You can also provide the primary key or id of the school alone instead of providing name and institution. Provide it for the key 'id'.
- Requires authentication: Yes
- Headers:
  - Key: Authorization
  - Value: Token <your_auth_token>
- Sample Response: Message indicating successful deletion.
- **Response when not authorized:**
    ```json
    {
        "error": "You are not authorized to DELETE this school. Only school-level admins can DELETE."
    }
    ```



### Department

#### Create Department
- Method: POST
- URL: `http://localhost:8000/institutions/department/`
- Requires authentication: Yes
- Headers:
  - Key: Authorization
  - Value: Token `<your_auth_token>`
- Request Data Example:
    ```json
    {
        "name": "<department_name>",
        "admins": ["<department_admin1_username>"]
    }
    ```
- Sample Response:
    ```json
    {
        "id": <department_id>,
        "courses": [],
        "lecturers": [],
        "head": null,
        "secretary": null,
        "created_by": "<created_by_username>",
        "admins": ["<created_by_username>", "<department_admin1_username>"],
        "school": "<school_name>",
        "name": "<department_name>"
    }
    ```
- Note: The 'school' field is automatically filled based on the institution the user is an admin of.

#### Get Department
- Method: GET
- URL: `http://localhost:8000/institutions/department/retrieve_department/?name=<department_name>&institution=<institution_name>`
- `NOTE:` You can also provide the primary key or id of the department alone instead of providing name and institution. Provide it for the key 'id'.
- Requires authentication: Yes

#### Update Department
- Method: PUT
- URL: `http://localhost:8000/institutions/department/update_department/?name=<department_name>&institution=<institution_name>`
- `NOTE:` You can also provide the primary key or id of the department alone instead of providing name and institution. Provide it for the key 'id'.
- Requires authentication: Yes
- Headers:
  - Key: Authorization
  - Value: Token `<your_auth_token>`
- Sample Request Data:
    ```json
    {
        "head": "<new_head_username>",
        "remove_admins": ["<department_admin1_username>"],
        "admins": ["<department_admin3_username>"]
    }
    ```
- Sample Response: Updated department details.
    ```json
    {
        "id": <department_id>,
        "courses": [],
        "lecturers": [],
        "head": "<new_head_username>",
        "secretary": null,
        "created_by": "<created_by_username>",
        "admins": ["<created_by_username>", "<department_admin2_username>", "<department_admin3_username>"],
        "school": "<school_name>",
        "name": "<department_name>"
    }
    ```
- Response when not authorized:
    ```json
    {
        "error": "You are not authorized to update this department. Only department-level admins can update."
    }

#### Delete Department
- Method: DELETE
- URL: `http://localhost:8000/institutions/department/delete_department/?name=<department_name>&institution=<institution_name>`
- `NOTE:` You can also provide the primary key or id of the department alone instead of providing name and institution. Provide it for the key 'id'.
- Requires authentication: Yes
- Headers:
  - Key: Authorization
  - Value: Token `<your_auth_token>`
- Sample Response: Message indicating successful deletion.
- Response when not authorized:
    ```json
    {
        "error": "You are not authorized to DELETE this department. Only department-level admins can DELETE."
    }



### Course

#### Create Course
- Method: POST
- URL: `http://localhost:8000/institutions/course/`
- Requires authentication: Yes
- Headers:
  - Key: Authorization
  - Value: Token `<your_auth_token>`
- Request Data Example:
    ```json
    {
        "name": "Bachelor of Commerce"
    }
    ```
- Sample Response:
    ```json
    {
        "id": 4,
        "created_by": "<created_by_username>",
        "department": "<user_department>",
        "school": "Business",
        "institution": "<user_institution>",
        "name": "Bachelor of Commerce"
    }
    ```
- `Note:` The user in the request can only create courses for the department they are an admin in.

#### Get Course
- Method: GET
- URL: `http://localhost:8000/institutions/course/retrieve_course/?name=Bachelor of Commerce&institution=<user_institution>`
- `NOTE:` You can also provide the primary key or id of the course alone instead of providing name and institution. Provide it for the key 'id'.
- Requires authentication: Yes
- Headers:
  - Key: Authorization
  - Value: Token `<your_auth_token>`
- Sample Response:
    ```json
    [
      {
        "id": 4,
        "created_by": "<created_by_username>",
        "department": "<user_department>",
        "school": "<user_school>",
        "institution": "<user_institution>",
        "name": "Bachelor of Commerce"
    }
    ]
    ```
- **Response when no institution provided:**
    ```json
    [
        {
            "id": 4,
            "created_by": "<created_by_username>",
            "department": "<user_department>",
            "school": "<user_school>",
            "institution": "<user_institution>",
            "name": "Bachelor of Commerce"
        },
        // ... Other courses with the same name in different institutions
    ]
    ```

#### Update Course
- Method: PUT
- URL: `http://localhost:8000/institutions/course/update_course/?name=Bachelor of Commerce&institution=<user_institution>`
- `NOTE:` The name of the course and the institution are to be provided in the query parameters.
- `NOTE:` You can also provide the primary key or id of the course alone instead of providing name and institution. Provide it for the key 'id'.
- Requires authentication: Yes
- Headers:
  - Key: Authorization
  - Value: Token `<your_auth_token>`
- Sample Request Data:
    ```json
    {
        "name": "Bachelor of Commerce Revised"
    }
    ```
- Sample Response: Updated course details.
    ```json
    [{
        "id": 4,
        "created_by": "<created_by_username>",
        "department": "<user_department>",
        "school": "<user_school>",
        "institution": "<user_institution>",
        "name": "Bachelor of Commerce Revised"
    }]
    ```
- **Response when not authorized:**
    ```json
    {
        "error": "You are not authorized to update this course. Only department-level admins can update."
    }
    ```

#### Delete Course
- Method: DELETE
- URL: `http://localhost:8000/institutions/course/delete_course/?name=Bachelor of Commerce&institution=<user_institution>`
- `NOTE:` The name of the course and the institution are to be provided in the query parameters.
- `NOTE:` You can also provide the primary key or id of the course alone instead of providing name and institution. Provide it for the key 'id'.
- Requires authentication: Yes
- Headers:
  - Key: Authorization
  - Value: Token `<your_auth_token>`
- Sample Response: Message indicating successful deletion.
- **Response when not authorized:**
    ```json
    {
        "error": "You are not authorized to DELETE this course. Only department-level admins can DELETE."
    }
    ```

### Unit

#### Create Unit
- Method: POST
- URL: `http://localhost:8000/institutions/unit/`
- Requires authentication: Yes
- Headers:
  - Key: Authorization
  - Value: Token `<your_auth_token>`
- Request Data Example:
    ```json
    {
        "name": "accounting",
        "course": "Bachelor of Commerce"
    }
    ```
- Sample Response:
    ```json
    {
        "id": 3,
        "course": "Bachelor of Commerce",
        "created_by": "<created_by_username>",
        "department": "<user_department>",
        "school": "<user_school>",
        "institution": "<user_institution>",
        "name": "accounting"
    }
    ```
- `Note:` The user in the request can only create units for courses offered by the department they are an admin in.

#### Get Unit
- Method: GET
- URL: `http://localhost:8000/institutions/unit/retrieve_unit/?name=accounting&institution=<user_institution>&course=Bachelor of Commerce`
- `NOTE:` You can also provide the primary key or id of the unit alone instead of providing name, course, and institution. Provide it for the key 'id'.
- Requires authentication: Yes
- Headers:
  - Key: Authorization
  - Value: Token `<your_auth_token>`
- Sample Response:
    ```json
    [
        {
            "id": 3,
            "course": "Bachelor of Commerce",
            "created_by": "<created_by_username>",
            "department": "<user_department>",
            "school": "<user_school>",
            "institution": "<user_institution>",
            "name": "accounting"
        }
    ]
    ```
- **Response when no institution and course provided:**
    ```json
    [
        {
            "id": 3,
            "course": "Bachelor of Commerce",
            "created_by": "<created_by_username>",
            "department": "<user_department>",
            "school": "<user_school>",
            "institution": "<user_institution>",
            "name": "accounting"
        },
        // ... Other units with the same name in different courses or institutions
    ]
    ```

#### Update Unit
- Method: PUT
- URL: `http://localhost:8000/institutions/unit/update_unit/?name=accounting&institution=<user_institution>&course=Bachelor of Commerce`
- `NOTE:` You can also provide the primary key or id of the unit alone instead of providing name, course, and institution. Provide it for the key 'id'.
- Requires authentication: Yes
- Headers:
  - Key: Authorization
  - Value: Token `<your_auth_token>`
- Sample Request Data:
    ```json
    {
        "name": "accounting101"
    }
    ```
- Sample Response: Updated unit details.
    ```json
    [
        {
            "id": 3,
            "course": "Bachelor of Commerce",
            "created_by": "<created_by_username>",
            "department": "<user_department>",
            "school": "<user_school>",
            "institution": "<user_institution>",
            "name": "accounting101"
        }
    ]
    ```
- **Response when not authorized:**
    ```json
    {
        "error": "You are not authorized to update this unit. Only department-level admins can update."
    }
    ```

#### Delete Unit
- Method: DELETE
- URL: `http://localhost:8000/institutions/unit/delete_unit/?name=accounting&institution=<user_institution>&course=Bachelor of Commerce`
- `NOTE:` You can also provide the primary key or id of the unit alone instead of providing name, course, and institution. Provide it for the key 'id'.
- Requires authentication: Yes
- Headers:
  - Key: Authorization
  - Value: Token `<your_auth_token>`
- Sample Response: Message indicating successful deletion.
- **Response when not authorized:**
    ```json
    {
        "error": "You are not authorized to DELETE this unit. Only department-level admins can DELETE."
    }
    ```







## Clubs and Societies App
### ClubSociety

#### Create Club/Society
- Method: POST
- URL: `http://localhost:8000/clubs_societies/clubsociety/`
- Requires authentication: Yes
- Headers:
  - Key: Authorization
  - Value: Token `<your_auth_token>`
- Request Data Example:
    ```json
    {
        "name": "<club_name>",
        "institution": "<institution_name>",
        "admins": ["<admin1_username>", "<admin2_username>"]
    }
    ```
- Sample Response:
    ```json
    {
        "id": <club_id>,
        "institution": "<institution_name>",
        "members": ["<admin1_username>", "<admin2_username>", "<created_by_username>"],
        "created_by": "<created_by_username>",
        "admins": ["<admin1_username>", "<admin2_username>"],
        "name": "<club_name>",
        "avatar": null,
        "bio": "",
        "location": "",
        "contact_number": "",
        "website": "",
        "facebook": "",
        "twitter": "",
        "instagram": "",
        "tiktok": "",
        "linkedin": "",
        "youtube": ""
    }
    ```

#### Get Club/Society
- Method: GET
- URL: `http://localhost:8000/clubs_societies/clubsociety/retrieve_club/?name=<club_name>&institution=<institution_name>`
- `NOTE:` You can also provide the primary key or id of the clubsociety alone instead of providing name and institution. Provide it for the key 'id'.
- Requires authentication: Yes
- Headers:
  - Key: Authorization
  - Value: Token `<your_auth_token>`

#### Update Club/Society
- Method: PUT
- URL: `http://localhost:8000/clubs_societies/clubsociety/update_club/?name=<club_name>&institution=<institution_name>`
- `NOTE:` You can also provide the primary key or id of the clubsociety alone instead of providing name and institution. Provide it for the key 'id'.
- Requires authentication: Yes
- Headers:
  - Key: Authorization
  - Value: Token `<your_auth_token>`
- Sample Request Data:
    ```json
    {
        "remove_members": ["<admin1_username>"]
    }
    ```
- Sample Response:
    ```json
    {
        "id": <club_id>,
        "institution": "<institution_name>",
        "members": ["<admin2_username>", "<created_by_username>"],
        "created_by": "<created_by_username>",
        "admins": ["<admin2_username>"],
        "name": "<club_name>",
        "avatar": null,
        "bio": "",
        "location": "",
        "contact_number": "",
        "website": "",
        "facebook": "",
        "twitter": "",
        "instagram": "",
        "tiktok": "",
        "linkedin": "",
        "youtube": ""
    }
    ```
- When a member is removed, their admin status is revoked,
- The user who creates the club cannot be removed.
- To revoke admin status without removing the members, use:
    ```json
    {
        "remove_admins": ["<admin1_username>"]
    }
    ```

#### Delete Club/Society
- Method: DELETE
- URL: `http://localhost:8000/clubs_societies/clubsociety/delete_club/?name=<club_name>&institution=<institution_name>`
- `NOTE:` You can also provide the primary key or id of the clubsociety alone instead of providing name and institution. Provide it for the key 'id'.
- Requires authentication: Yes
- Headers:
  - Key: Authorization
  - Value: Token `<your_auth_token>`






## Lecturers App
### Lecturer

#### Create Lecturer
- Method: POST
- URL: `http://localhost:8000/lecturers/lecturer/`
- Requires authentication: Yes (Token should be provided in the header)
- Request Data Example:
    ```json
    {
        "institution": "<institution_name>",
        "departments": ["<department1_name>"]
    }
    ```
- Sample Response: The response data contains lecturer status information along with profile information of the user. 
    ```json
    {
        "id": <lecturer_id>,
        "user": "<username>",
        "profile": {
            "avatar": null,
            "bio": "bio for <username>",
            "location": "",
            "contact_number": "",
            "website": "",
            "facebook": "",
            "twitter": "",
            "instagram": "",
            "tiktok": "",
            "linkedin": "",
            "youtube": ""
        },
        "institution": "<institution_name>",
        "departments": [
            "<department1_name>"
        ]
    }
    ```

#### Get Lecturer
- Method: GET
- URL: `http://localhost:8000/lecturers/lecturer/retrieve_lecturer/?username=<username>`
- Requires authentication: Yes (Token should be provided in the header)
- Sample Response:
    ```json
    {
        "id": <lecturer_id>,
        "user": "<username>",
        "profile": {
            "avatar": null,
            "bio": "bio for <username>",
            "location": "",
            "contact_number": "",
            "website": "",
            "facebook": "",
            "twitter": "",
            "instagram": "",
            "tiktok": "",
            "linkedin": "",
            "youtube": ""
        },
        "institution": "<institution_name>",
        "departments": [
            "<department1_name>"
        ]
    }
    ```

#### Update Lecturer
- Method: PUT
- URL: `http://localhost:8000/lecturers/lecturer/update_lecturer/`
- Requires authentication: Yes (Token should be provided in the header)
- Request Data Example:
    ```json
    {
        "remove_departments": ["<department1_name>"],
        "departments": ["<department2_name>"]
    }
    ```
- Sample Response: The response data contains lecturer status information along with profile information of the user.
    ```json
    {
        "id": <lecturer_id>,
        "user": "<username>",
        "profile": {
            "avatar": null,
            "bio": "bio for <username>",
            "location": "",
            "contact_number": "",
            "website": "",
            "facebook": "",
            "twitter": "",
            "instagram": "",
            "tiktok": "",
            "linkedin": "",
            "youtube": ""
        },
        "institution": "<institution_name>",
        "departments": [
            "<department2_name>"
        ]
    }
    ```
- `NOTE:` Only the user in the request can update their lecturer status.

#### Delete Lecturer
- Method: DELETE
- URL: `http://localhost:8000/lecturers/lecturer/delete_lecturer/`
- Requires authentication: Yes (Token should be provided in the header)
- `NOTE:` Only the user in the request can delete their lecturer status. This does not delete the user, only their status as a lecturer.





## Notes App

### Categories

#### Create Categories in Bulk
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

#### Create Single Category
- Method: POST
- URL: `http://localhost:8000/notes/categories/create/`
- Request Data Example:
    ```json
    {
        "name": "Business"
    }
    ```

#### Get Categories
- Method: GET
- URL: `http://localhost:8000/notes/categories/`

#### Delete Category by ID
- Method: DELETE
- URL: `http://localhost:8000/notes/categories/<category_id>/`

#### Delete Category by Name
- Method: DELETE
- URL: `http://localhost:8000/notes/categories/delete_by_name/<category_name>/`

#### Delete Categories in Bulk
- Method: DELETE
- URL: `http://localhost:8000/notes/categories/bulk_delete/`
- Request Data Example:
    ```json
    {
        "category_names": ["Mathematics", "Music", "Engineering"]
    }
    ```

### Documents

#### Upload Document
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

#### Download Document by ID
- Method: GET
- URL: `http://localhost:8000/notes/documents/<document_id>/download_document_by_id/`
- Note: Authentication details are required in the header.
    - Key: Authorization
    - Value: Token <your_auth_token>

#### Download Document by Title
- Method: GET
- URL: `http://localhost:8000/notes/documents/<document_title>/download_document_by_title/`
- Note: Authentication details are required in the header.
    - Key: Authorization
    - Value: Token <your_auth_token>

#### Download URLs for All Documents
- Method: GET
- URL: `http://localhost:8000/notes/documents/document_urls/`
- Note: Authentication details are required in the header.
    - Key: Authorization
    - Value: Token <your_auth_token>

#### Download URLs by Document IDs
- Method: GET
- URL: `http://localhost:8000/notes/documents/document_urls/?ids=<document_id_1>,<document_id_2>`
- Note: Authentication details are required in the header.
    - Key: Authorization
    - Value: Token <your_auth_token>

#### Download URLs by Document Titles
- Method: GET
- URL: `http://localhost:8000/notes/documents/document_urls/?titles=<document_title_1>,<document_title_2>`
- Note: Authentication details are required in the header.
    - Key: Authorization
    - Value: Token <your_auth_token>

### Topics

#### Create Topic
- Method: POST
- URL: `http://localhost:8000/notes/topics/create_topic/`
- Request Data Example:
    - Form Data:
        - Keys: `document_title` (optional), `start_page` (optional), `end_page` (optional), `uploaded_document` (file)
    - Note: Either `document_title` or `uploaded_document` must be provided. If both are provided, a document is created with the provided title and the topic is associated with that document. If only one is provided, the code attempts to find an existing document or create a new one.
    - Note: Authentication details are required in the header.
        - Key: Authorization
        - Value: Token <your_auth_token>

#### Get All Topics
- Method: GET
- URL: `http://localhost:8000/notes/topics/`
- Note: Authentication details are required in the header.
    - Key: Authorization
    - Value: Token <your_auth_token>

#### Get Topic by ID
- Method: GET
- URL: `http://localhost:8000/notes/topics/<topic_id>/`
- Note: Authentication details are required in the header.
    - Key: Authorization
    - Value: Token <your_auth_token>

#### Get Topics by Name
- Method: GET
- URL: `http://localhost:8000/notes/topics/<topic_name>/`
- Note: Authentication details are required in the header.
    - Key: Authorization
    - Value: Token <your_auth_token>

#### Update Topic
- Method: PUT
- URL: `http://localhost:8000/notes/topics/update_topic/?topic_name=<topic_name>&document_title=<document_title>`
- Request Data Example (Form Data): Fields to be updated.
    - Note: Parameters are provided in the query.
    - Note: Authentication details are required in the header.
        - Key: Authorization
        - Value: Token <your_auth_token>

#### Delete Topic
- Method: DELETE
- URL: `http://localhost:8000/notes/topics/delete_topic/?topic_name=<topic_name>&document_title=<document_title>`
- Note: Parameters are provided in the query.
- Note: Authentication details are required in the header.
    - Key: Authorization
    - Value: Token <your_auth_token>

### Lectures

#### Create Lecture
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
- Note: Authentication details are required in the header.
    - Key: Authorization
    - Value: Token <your_auth_token>

#### Get All Lectures
- Method: GET
- URL: `http://localhost:8000/notes/lectures/`
- Note: Authentication details are required in the header.
    - Key: Authorization
    - Value: Token <your_auth_token>

#### Get Lecture by ID
- Method: GET
- URL: `http://localhost:8000/notes/lectures/<lecture_id>/`
- Note: Authentication details are required in the header.
    - Key: Authorization
    - Value: Token <your_auth_token>

#### Update Lecture by ID
- Method: PUT
- URL: `http://localhost:8000/notes/lectures/update_lecture/`
- Request Data Example:
    ```json
    {
        "id": 21,
        "topics": [1, 9]
    }
    ```
- Note: Authentication details are required in the header.
    - Key: Authorization
    - Value: Token <your_auth_token>

#### Update Lecture by Query Parameters
- Method: PUT
- URL: `http://localhost:8000/








## Testing API endpoints

To interact with the API endpoints for your newly created project, you can use tools like [Postman](https://www.postman.com/) to send HTTP requests to the API endpoints. Here's how you can use Postman:

1. Install Postman on your machine from the [Postman website](https://www.postman.com/downloads/).
2. Launch Postman and create a new request.
3. Set the request method (e.g., POST, GET) and URL for the desired API endpoint.
4. Add any required headers or request parameters.
5. Send the request and view the response.


Make sure to replace `http://localhost:8000/` in the API URL with the appropriate base URL if running the API on a different host or port.