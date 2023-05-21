# CoolBox Backend

### Authorization: Bearer Token (SchoolBox)
# Endpoints

### GET /user
Returns user information

Responses: 200, 401

### GET /users
Returns general information of all users

Responses: 200, 401

---

### GET /quick-notes
Returns all quick notes

Responses: 200, 401

### PUT /quick-notes
Overrides ALL quick notes

Fields: Ordered list of objects(*Title, *Content)

Responses: 200, 400, 401, 500

---

### GET /reminders
Returns all reminders

Responses: 200, 401

### POST /reminders
Create a new reminder

Fields: *Title, *Due, *Method, Assessment

Responses: 200, 400, 401

### PATCH /reminders
Edit an existing reminder

Fields: *Id, Title, Due, Method, Assessment

Responses: 200, 400, 401, 404


### DELETE /reminders
Delete a reminder

Fields: *Id

Responses: 200, 400, 401, 404

---

### REDIRECT /discord/redirect
Link discord account

Responses: 302, 401

### DELETE /discord
Unlink discord account

Responses: 200, 401, 404

---

### GET /stats/running
Get machine uptime, also used for monitoring

Responses: 200


### GET /stats/user_count
Get user count

Responses: 200


### GET /stats/message
Get status message

Responses: 200, 401

---

### POST /subjects
Add & retrieve subjects 

Fields: List of objects(*name)

Responses: 200, 400, 401

