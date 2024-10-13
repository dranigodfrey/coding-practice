import React from 'react';
import { useNavigate } from 'react-router-dom';

const Page404 = () => {
	const navigate = useNavigate();
	return (
		<div>
			<p>404 | Page Not Found.</p>
			<button onClick={() => navigate('/home')}>Go back Home</button>
		</div>
	);
};

export default Page404;
