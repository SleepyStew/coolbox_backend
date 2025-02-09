# CoolBox Backend

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=SleepyStew_coolbox_backend&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=SleepyStew_coolbox_backend)
[![Django CI](https://github.com/SleepyStew/coolbox_backend/actions/workflows/django.yml/badge.svg)](https://github.com/SleepyStew/coolbox_backend/actions/workflows/django.yml)

### Authorization: Bearer Token (SchoolBox)

### All endpoint specific responses should have error handling

# Endpoints

### GET /user
Returns user information

General Responses: 200, 401

---

### GET /quick-notes
Returns all quick notes

General Responses: 200, 401

### PUT /quick-notes
Overrides ALL quick notes

Fields: Ordered list of objects(*Title, *Content)

General Responses: 200, 400, 401

Endpoint Specific Responses: 500

---

### GET /reminders
Returns all reminders

General Responses: 200, 401

### POST /reminders
Create a new reminder

Fields: *Title, *Due, *Method, Assessment

General Responses: 200, 400, 401

### PATCH /reminders
Edit an existing reminder

Fields: *Id, Title, Due, Method, Assessment

General Responses: 200, 400, 401

Endpoint Specific Responses: 404


### DELETE /reminders
Delete a reminder

Fields: *Id

General Responses: 200, 400, 401

Endpoint Specific Responses: 404

---

### REDIRECT /discord/redirect
Link discord account

General Responses: 401

Endpoint Specific Responses: 302

### DELETE /discord
Unlink discord account

General Responses: 200, 401

Endpoint Specific Responses: 404

---

### GET /stats/running
Get machine uptime, also used for monitoring

General Responses: 200


### GET /stats/user_count
Get user count

General Responses: 200


### GET /stats/message
Get status message

General Responses: 200, 401

---

### POST /subjects
Add & retrieve subjects 

Fields: List of objects(*name)

General Responses: 200, 400, 401

---

### POST /feedback
Send feedback

Fields: *Content, *Origin, Anonymous

General Responses: 200, 400, 401

Endpoint Specific Responses: 429, 500

---

### GET /room-changes
Get today's room changes

General Responses: 200, 401

---

### GET /weather
Get current weather

General Responses: 200, 401

Endpoint Specific Responses: 500

---

### GET /start
Collates needed data for initial page load

This endpoint makes ~6 internal requests, beware of ratelimit.

General Responses: 200, 401

---

### POST /error-report
Submit an automatic error report

Fields: *Error, Detail

General Responses: 200, 400, 401

---

### GET /daily-message/verse
Get daily bible verse

General Responses: 200, 401

Endpoint Specific Responses: 404

---

### GET /tasks
Get all tasks

General Responses: 200, 401

### POST /tasks

Create a new task

Fields: *Title, *Due, Subject, *Type

Subject should be in NON-prettified form

General Responses: 200, 400, 401

### PATCH /tasks

Edit an existing task

Fields: *Id, Title, Due, Subject, Type

Subject should be in NON-prettified form

General Responses: 200, 400, 401

Endpoint Specific Responses: 404

### DELETE /tasks

Delete a task

Fields: *Id

General Responses: 200, 400, 401

Endpoint Specific Responses: 404

---

### GET /assessment-notes

Get all assessment notes

General Responses: 200, 401

### POST /assessment-notes

Create a new assessment note

Fields: *Assessment, *Content, 

Assessment should be ID form

General Responses: 200, 400, 401

### PATCH /assessment-notes

Edit an existing assessment note

Fields: *Id, Assessment, Content

General Responses: 200, 400, 401

Endpoint Specific Responses: 404

### DELETE /assessment-notes

Delete an assessment note

Fields: *Id

General Responses: 200, 400, 401

Endpoint Specific Responses: 404

---

### GET /todos

Get all todos, includes items

General Responses: 200, 401

### POST /todos

Create a new todo

Fields: *Title

General Responses: 200, 400, 401

### PATCH /todos

Edit an existing todo

Fields: *Id, Title

General Responses: 200, 400, 401

Endpoint Specific Responses: 404

### DELETE /todos

Delete a todo

Fields: *Id

General Responses: 200, 400, 401

Endpoint Specific Responses: 404

### PUT /todos

Override todo items (and order) for a todo

Fields: *Id, *Items (List of objects(*Content))

General Responses: 200, 400, 401

Endpoint Specific Responses: 404

---