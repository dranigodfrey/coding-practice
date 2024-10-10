import React from 'react';
import { useLoaderData } from 'react-router-dom';

const JobDetail = () => {
	const jobDetail = useLoaderData();
	return (
		<div>
			<p>
				<b>Job Title:</b>
				{jobDetail.title}
			</p>
			<p>
				<b>Salary:</b>
				{jobDetail.salary}
			</p>
			<p>
				<b>Location:</b>
				{jobDetail.location}
			</p>
			<button>Apply Now!</button>
		</div>
	);
};

export default JobDetail;

export const jobDetailLoader = async ({ params }) => {
	const { id } = params;
	const response = await fetch('http://localhost:5000/jobs/' + id);
	if (!response.ok) {
		throw Error('Could not found job details');
	}
	return response.json();
};
