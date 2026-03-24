import Main from './components/Main'
import Profile from './pages/Profile'
import Login from './pages/Login'
import Register from './pages/Register'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Games from './pages/Games'
import Game from './pages/Game'
import ProtectedRoute from './components/ProtectedRoute'
import GamesPage from './components/GamesPage' // страница поиска

function App() {
	return (
		<Router>
			<Routes>
				<Route path='/' element={<Main />} />
				<Route
					path='/profile'
					element={
						<ProtectedRoute>
							<Profile />
						</ProtectedRoute>
					}
				/>
				<Route path='/login' element={<Login />} />
				<Route path='/register' element={<Register />} />
				<Route path='/games' element={<Games />} /> // список всех игр
				<Route path='/game/:id' element={<Game />} /> // детальная страница игры
				<Route path='/search' element={<GamesPage />} /> // результаты поиска
			</Routes>
		</Router>
	)
}

export default App
