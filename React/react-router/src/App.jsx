import {
	Route,
	createBrowserRouter,
	createRoutesFromElements,
	RouterProvider,
} from 'react-router-dom';
import Home from './pages/Home';
import Product from './pages/Product';
import About from './pages/About';
import RootLayout from './layout/RootLayout';
import ContactLayout from './layout/ContactLayout';
import ContactForm from './components/ContactForm';
import ContactInfo from './components/ContactInfo';
import NotFound from './components/NotFound';
import JobsLayout from './layout/JobsLayout';
import Jobs, { jobsLoader } from './pages/Jobs';
import JobDetail, { jobDetailLoader } from './components/JobDetail';
import Error from './components/Error';

function App() {
	const router = createBrowserRouter(
		createRoutesFromElements(
			<Route
				path='/'
				element={<RootLayout />}
			>
				<Route
					index
					element={<Home />}
				/>
				<Route
					path='products'
					element={<Product />}
				/>
				<Route
					path='about'
					element={<About />}
				/>
				<Route
					path='contact'
					element={<ContactLayout />}
				>
					<Route
						path='form'
						element={<ContactForm />}
					/>
					<Route
						path='info'
						element={<ContactInfo />}
					/>
				</Route>
				<Route
					path='jobs'
					element={<JobsLayout />}
					errorElement={<Error />}
				>
					<Route
						index
						element={<Jobs />}
						loader={jobsLoader}
					/>
					<Route
						path=':id'
						element={<JobDetail />}
						loader={jobDetailLoader}
					/>
				</Route>
				<Route
					path='*'
					element={<NotFound />}
				/>
			</Route>
		)
	);

	return <RouterProvider router={router} />;
}

export default App;
