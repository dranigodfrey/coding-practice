import Root from './layouts/Root';
import PageNotFound from './components/PageNotFound';
import About from './pages/About';
import Contact from './pages/Contact';
import Home from './pages/Home';
import ContactForm from './components/ContactForm';
import ContactInfo from './components/ContactInfo';
import {
	createBrowserRouter,
	createRoutesFromElements,
	Route,
} from 'react-router-dom';
import HomeLayout from './layouts/HomeLayout';

export const router = createBrowserRouter(
	createRoutesFromElements(
		<Route
			path='/'
			element={<Root />}
			errorElement={<PageNotFound />}
		>
			<Route
				index
				element={<HomeLayout />}
			/>
			<Route
				path='home'
				element={<Home />}
			>
				<Route
					path='info'
					element={<ContactInfo />}
				/>
				<Route
					path='form'
					element={<ContactForm />}
				/>
			</Route>
			<Route
				path='about'
				element={<About />}
			/>
			<Route
				path='contact'
				element={<Contact />}
			/>
		</Route>
	)
);
