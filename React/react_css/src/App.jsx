import { useState } from 'react';
import './App.scss';

function App() {
	const [count, setCount] = useState(0);

	return (
		<section className='container'>
			<header className='box'>1</header>
			<aside className='box'>2</aside>
			<main className='box'>3</main>
			<footer className='box'>4</footer>
		</section>
	);
}

export default App;
