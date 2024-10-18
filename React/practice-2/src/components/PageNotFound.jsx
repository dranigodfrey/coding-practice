import React from 'react';
import { useNavigate } from 'react-router-dom';

const PageNotFound = () => {
	const navigate = useNavigate();
	return (
		<div>
			<h3>404 | Page not Found.</h3>
			<button onClick={() => navigate('/')}>Go To Home Page</button>
		</div>
	);
};

export default PageNotFound;
