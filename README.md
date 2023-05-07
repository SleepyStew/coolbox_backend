# CoolBox Backend

### Authorization: Bearer Token (SchoolBox)
## Endpoints

### GET /user
Returns user information

### GET /quick-notes
Returns all quick notes

### POST /quick-notes
Overrides ALL quick notes

Fields: Ordered list of objects(Title, Content)


### GET /reminders
Returns all reminders

### POST /reminders
Create a new reminder

Fields: Title, Due, Method

### DELETE /reminders
Delete a reminder

Fields: Id

### DELETE /discord
Unlink discord account
