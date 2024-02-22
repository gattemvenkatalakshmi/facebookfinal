### Software Requirements
#### User Persona
- Name: G.Venkata Lakshmi
    -  Why Facebook ?
        -  to know about her friends.
        -  to  post pictures.
        -  to  follow celebreties.
        -  to watch funny memes.
        - to send friends.
        - to make online friends.
- Name :  Content Creator/ famous Celebrity
    -  why facebook?
        - To  Update  fans
        - To get more famous
        - To  do promotions
        - To entertain people.
    
#### User Stories
- As a User  I should be able to create an account
 - As a User  I should be able to login into my account
 - As a User  I should be able to  send friend request
 - As a User  I should be able to  remove friends 
 - As a User  I should be able to view my friends
 - As a User  I should be able to  post a picture
 - As a User  I should be able to  post a  videos
 - As a User  I should be able to  cancel friend Request
 - As a User  I should be able to   message my friends
 - As a User  I should be able to  delete my post 
 - As a User  I should be able to like to my friend post
 - As a User  I should be able to comment on my friend post
 - As a User  I should be able to  delete account
 - As a User  I should be able to logout of the account
- As a User  I should be able to  keep my account private or public
- As a user  I should be able to view my friends  posts.
#### Table Schemas
 - users 
     - ID
     - FirstName
     - LastName
     - Phone Number
     - Date Of Birth
     - Gender
 - friends
    - friend_id
    - userid( foreignkey)
 - posts of Users
     - user id( foreign key)
     - post
     - post time
     - likes 
     - comments
     