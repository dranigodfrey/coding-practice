import React from 'react';
import { Outlet, Link, useNavigate, NavLink } from 'react-router-dom';
import Home from '../pages/Home';

const HomeLayout = () => {
	const navigate = useNavigate();
	return (
		<div>
			<h1>home layout</h1>
			<Home />
			<Outlet />
		</div>
	);
};

export default HomeLayout;
