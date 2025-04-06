// Button.jsx
import './Button.scss';

function Button({ children, variant }) {
	return <button className={`button ${variant}`}>{children}</button>;
}

export default Button;
