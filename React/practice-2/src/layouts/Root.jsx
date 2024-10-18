import React from 'react';
import NavBar from '../components/NavBar';
import { Outlet } from 'react-router-dom';

const Root = () => {
	return (
		<div className='container'>
			<header>
				<NavBar />
			</header>
			<main>
				<Outlet />
			</main>
		</div>
	);
};

export default Root;
