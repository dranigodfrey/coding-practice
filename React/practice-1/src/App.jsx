import React from 'react';
import Home from './pages/Home';
import {
	createBrowserRouter,
	createRoutesFromElements,
	Route,
	RouterProvider,
} from 'react-router-dom';
import About from './pages/About';
import Contact from './pages/Contact';
import NavBar from './components/NavBar';
import MainLayout from './layouts/MainLayout';
import HomeLayout from './layouts/HomeLayout';
import Page404 from './components/Page404';
import News from './components/News';

const App = () => {
	const router = createBrowserRouter([
		{
			path: '/',
			element: <MainLayout />,
			errorElement: <Page404 />,
			children: [
				{
					path: '/home',
					element: <HomeLayout />,
					children: [
						{
							index: true,
							element: <Home />,
						},
					],
				},
				{
					path: '/about',
					element: <About />,
				},
				{
					path: '/contact',
					element: <Contact />,
				},
			],
		},
	]);

	return (
		<div className='container'>
			<RouterProvider router={router} />
		</div>
	);
};

export default App;
