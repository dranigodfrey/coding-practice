import React from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import Logo from '../assets/bing_logo.png';

const Navbar = () => {
	const navigate = useNavigate();
	return (
		<div className='navbar'>
			<img
				src={Logo}
				alt='company logo'
				width='40px'
			/>
			<ul>
				<NavLink to='/'>
					<li>Home</li>
				</NavLink>
				<NavLink to='/about'>
					<li>About</li>
				</NavLink>
				<NavLink to='/contact'>
					<li>Contact</li>
				</NavLink>
				<NavLink to='/products'>
					<li>Product</li>
				</NavLink>
				<NavLink to='/jobs'>
					<li>Jobs</li>
				</NavLink>
			</ul>
			<button onClick={() => navigate('/about', { replace: true })}>
				Get Started
			</button>
		</div>
	);
};

export default Navbar;
