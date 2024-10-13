import React from 'react';
import { NavLink } from 'react-router-dom';

const NavBar = () => {
	return (
		<div>
			<ul>
				<NavLink to='/home'>
					<li>Home</li>
				</NavLink>
				<NavLink to='/about'>
					<li>About</li>
				</NavLink>
				<NavLink to='/contact'>
					<li>Contact</li>
				</NavLink>
			</ul>
		</div>
	);
};

export default NavBar;
