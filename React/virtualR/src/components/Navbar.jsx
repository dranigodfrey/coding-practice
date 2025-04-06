import React from 'react';
import logo from '../assets/logo.png';
const Navbar = () => {
	return (
		<nav className='sticky top-0 z-50 py-3 backdrop-blur-lg border-b border-neutral-700/80'>
			<div className='container px-4 mx-auto relative text-sm'>
				<div className='flex justify-center items-center'>
					<img
						className='w-10 h-10 mr-2'
						src={logo}
						alt='logo'
					/>
					<span className='text-xl tracking-tight'>VirtualR</span>
				</div>
			</div>
		</nav>
	);
};

export default Navbar;
