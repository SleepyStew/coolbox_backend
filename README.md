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

### REDIRECT DiscordOAuth
Link discord account

Responses: 401, 302

https://discord.com/oauth2/authorize?client_id=999205944133177365&redirect_uri=https%3A%2F%2Fapi.coolbox.lol%2Fdiscord&response_type=code&scope=identify&state=TOKEN


### DELETE /discord
Unlink discord account

Responses: 200, 401, 404
