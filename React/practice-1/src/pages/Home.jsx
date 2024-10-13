import React from 'react';
import { Link, Outlet, useNavigate } from 'react-router-dom';

const Home = () => {
	const navigate = useNavigate();
	return (
		<div>
			<h1>Home page!</h1>
			<button onClick={() => navigate('/home/news')}>
				Go to About Page
			</button>
			<Outlet />
		</div>
	);
};

export default Home;
