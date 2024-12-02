import React from 'react'
import Nav from '../components/Nav'
import { Outlet } from 'react-router-dom'

const RootLayout = () => {
  return (
      <>
          <header>
              <Nav/>
          </header>
          <main>
              <Outlet/>
          </main>
      </>
  )
}

export default RootLayout