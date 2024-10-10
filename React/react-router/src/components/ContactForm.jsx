import React from 'react';

const ContactForm = () => {
	return (
		<div>
			<form action=''>
				<input
					type='text'
					placeholder='Name'
				/>
				<br />
				<input
					type='email'
					placeholder='Email'
				/>
				<br />
				<textarea
					name=''
					placeholder='message'
					id=''
				></textarea>
				<br />
				<button type='submit'>Send</button>
			</form>
		</div>
	);
};

export default ContactForm;
