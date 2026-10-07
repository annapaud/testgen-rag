# PRD-102: User Authentication & Security

## 1. Password Policy
- Passwords must be at least 8 characters and no more than 32 characters long.
- Must contain at least 1 uppercase letter, 1 number, and 1 special character (@, #, $, %).

## 2. Account Lockout
- After 3 consecutive failed login attempts, the account is locked for 15 minutes.
- A password reset link can be requested while the account is locked.
