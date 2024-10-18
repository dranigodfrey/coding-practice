import React from 'react';
import { Outlet, useNavigate } from 'react-router-dom';

const Home = () => {
	const navigate = useNavigate();
	return (
		<div>
			<p>Welcome to our home page!</p>
			<button onClick={() => navigate('info')}>View Info</button>
			<button onClick={() => navigate('form')}>View Form</button>
			<Outlet />
		</div>
	);
};

export default Home;
