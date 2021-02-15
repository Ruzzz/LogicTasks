Calculate the rating of the most active users based on the longest streak of posts.
The size of the streak for the user is the number of consecutive time intervals 
in which at least one post has been published by this user.

For example, if the user created posts on:

- 01 Sept. at 12:00,
- 02 Sept. at 14:00,
- 03 Sept. at 09:00,
- 05 Sept. at 10:00

Then at the interval size of 1 day, we can say that the longest streak of posts for this user is 3.
In other words, the user made at least one post for 3 consecutive days.

The interval should be passed as a query parameter and can be 24h or 1h.
