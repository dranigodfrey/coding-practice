import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import RootLayout from './layouts/RootLayout'
import Home from './pages/Home'
import PageNotFound from './pages/PageNotFound'
import SignIn from './pages/SignIn'
import SignUp from './pages/SignUp'

function App() {
  const router = createBrowserRouter(
    [
      {
        path: '/',
        element: <RootLayout />, 
        errorElement:<PageNotFound/>,
        children: [
          {
            index: true,
            element: <Home/>
          },
          {
            path: 'sign-in/',
            element: <SignIn/>
          },
          {
            path: 'sign-up/',
            element: <SignUp/>
          }
        ]
      }
    ]
  )

  return (
    <>
      <RouterProvider router={router} />
    </>
  )
}

export default App
