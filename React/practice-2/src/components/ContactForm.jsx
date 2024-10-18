import React from 'react';

const ContactForm = () => {
	return (
		<div>
			<form action=''>
				<div>
					<input
						type='email'
						name='email'
						placeholder='your email'
					/>
				</div>
				<div>
					<textarea
						name='text'
						id=''
					></textarea>
				</div>
				<div>
					<input
						type='submit'
						value='Send'
					/>
				</div>
			</form>
		</div>
	);
};

export default ContactForm;
