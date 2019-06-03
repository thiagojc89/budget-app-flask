# budget-app-flask

### User story
How many times did you look at your bills and was happy because you have money to pay them? Weird question am I right? Even when we pay our bills 
is hard to see something good from it.

A lot of people around the world don't realize that having money is a good thing, even if it is to pay bills.That does not mean that we should go crazy and dive into a pile of credit card statements loans and etc, but what we definitely can do is learn how to deal with our money.

Yeah! I said it, it's good to pay bills, that's is how things work, however not paying them can be very painful or when you have money to pay your bills but you pass the due date. So with that thinking, I decided to build this website to help those people (me) pay their bills on time and visualize their expenses in order to plan new acquisitions.

#### Navigation
1. Home Page will provide a login and sign-up option.

2. After login or sign up the user is redirected to his/her user page and should have the ability to perform these actions:
   * User should be able to add a deposit, it will require two entries (date, amount).
   * User should be able to update / delete a deposit.
   * The user should be able to add expenses to the budget, it will require two entries (date, amount).
   * User should be able to update / delete a expenses.

3. A chart would be placed in the center of the page giving a visualization by Amount(vertical axis) Vs Date (Horizontal axis).

4. The chart will use the registration date as the starting point.



### Route

| Method | Path | Action|
|--------|------|-------|
| POST | /auth/login | Login a user into the website |
| POST | /auth/register | Register a new user |
| GET | /user/budgetitem | Fecth user data to be present on sreen |
| POST | /user/budgetitem | add a new expenses to the budget |
| DELETE | /user/budgetitem | delete a expenses from user budget |
| PUT | /user/budgetitem | update a expenses from user budget |




### Models

#### 1. User
  * First Name
  * Last Name
  * Email
  * Password
  * Budget - relation with budget table
  * Balance

#### 2. Budget
  * Name
  * Itens

#### 3. Item
  * Name
  * Value
  * Due Date
  * Payment Date
    
