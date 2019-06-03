# budget-app-flask

## Route

| Method | Path | Action|
|--------|------|-------|
| GET | /auth/login | Login a user into the website |
| POST | /auth/register | Sign in a new user |
| DELETE | /auth/{user_id} | Delete user account |






# User story
1. Home Page will provide a login and sign-up option.

2. After login or sign up the user is redirected to his/her user page and should have the ability to perform these actions:
  * User should be able to add a deposit, it will require two entries (date, amount).
  * The user should be able to add expenses to the budget, it will require two entries (date, amount).

3. A chart would be placed in the center of the page giving a visualization of the money by Amount X Date.

4. The chart will use the registration date as a take the Date axis
