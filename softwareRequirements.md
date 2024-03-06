### Software Requirements

#### User Persona

- Name: G.Venkata Lakshmi
  - Why Facebook ?
    - to know about her friends.
    - to post pictures.
    - to follow celebreties.
    - to watch funny memes.
    - to send friends.
    - to make online friends.
- Name : Content Creator/ famous Celebrity
  - why facebook?
    - To Update fans
    - To get more famous
    - To do promotions
    - To entertain people.

#### User Stories

- As a User I should be able to create an account -done
- As a User I should be able to login into my account -done
- As a User I should be able to rest password -done
- As a User I should be able to logout of the account -done
- As a User I should be able to send friend request -done
- As a User I should be able to remove friends -done
- As a User I should be able to cancel friend Request -done
- As a User I should be able to view my friends -done
- As a User I should be able to post a picture -done
- As a User I should be able to post a videos -done
- As a User I should be able to delete my post 
- As a User I should be able to like to my friend post -done
- As a User I should be able to comment on my friend post
- As a User I should be able to delete account 
- As a user I should be able to  message my friends 
- As a User I should be able to keep my account private or public
- As a user I should be able to view my friends posts.

#### Table Schemas

- users
  - ID
  - FirstName
  - LastName
  - Phone Number
  - email
  - Date Of Birth
  - Gender
  - profile picture
    -friend_requests
    -from_user
    -to_user
- friendship
  -friendhip_id
  - friend_id
  - userid( foreignkey)
- posts of Users - user id( foreign key) - post - post time - likes count - comments count
  -likes - post_id - user_id
  -comments
  -post_id - user_id - comment_text
