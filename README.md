# CoolBox Backend

### Authorization: Bearer Token (SchoolBox)
# Endpoints

### GET /user
Returns user information

### GET /users
Returns general information of all users

---

### GET /quick-notes
Returns all quick notes

### POST /quick-notes
Overrides ALL quick notes

Fields: Ordered list of objects(Title, Content)

---

### GET /reminders
Returns all reminders

### POST /reminders
Create a new reminder

Fields: Title, Due, Method

### DELETE /reminders
Delete a reminder

Fields: Id

---

### REDIRECT DiscordOAuth
Link discord account

https://discord.com/oauth2/authorize?client_id=999205944133177365&redirect_uri=https%3A%2F%2Fapi.coolbox.lol%2Fdiscord&response_type=code&scope=identify&state=TOKEN

### DELETE /discord
Unlink discord account
