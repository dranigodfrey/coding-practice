import React from 'react'

const SignUp = () => {
  return (
     <>
          <h3>Sign Up</h3>
          <form action="">
              <div>
                  <label htmlFor="email">Email:</label>
                  <input type="email" id='email' placeholder='Enter your email address'/>
              </div>
               <div>
                  <label htmlFor="username">Username:</label>
                  <input type="text" id='username' placeholder='Enter your username'/>
              </div>
              <div>
                  <label htmlFor="password">Password:</label>
                  <input type="password" id='password' placeholder='Enter your password'/>
              </div>
              <div>
                  <input type="submit" id='submit' value='Sign In'/>
              </div>
          </form>
      </>
  )
}

export default SignUp