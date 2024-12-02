import React from 'react'
import { Route } from 'react-router-dom'

const PrivateRouter = ({ children, ...rest }) => {
    console.log('Private router works.')
  return (
      <Route {...rest}>{ children }</Route>
  )
}

export default PrivateRouter