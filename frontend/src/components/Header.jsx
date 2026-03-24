import React, { useState, useRef, useEffect } from 'react'
import S from '../style/Header.module.css'
import { NavLink, useNavigate } from 'react-router-dom'

export const Header = () => {
	const navigate = useNavigate()
	const [isOpen, setIsOpen] = useState(false)
	const [user, setUser] = useState(null)
	const menuRef = useRef(null)
	const [searchQuery, setSearchQuery] = useState('') // состояние для поиска

	// проверка авторизации при рендере хедера
	useEffect(() => {
		const checkAuth = () => {
			const savedName = localStorage.getItem('userName')
			const token = localStorage.getItem('userToken')
			setUser(token && savedName ? savedName : null)
		}

		checkAuth()
		window.addEventListener('authChange', checkAuth)
		window.addEventListener('storage', checkAuth)

		return () => {
			window.removeEventListener('authChange', checkAuth)
			window.removeEventListener('storage', checkAuth)
		}
	}, [])

	const handleLogout = async () => {
		const token = localStorage.getItem('userToken')

		try {
			await fetch('http://127.0.0.1:8000/api/core/logout/', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
					Authorization: `Token ${token}`,
				},
			})
		} catch (error) {
			console.error('Ошибка при логауте на сервере:', error)
		}

		localStorage.removeItem('userToken')
		localStorage.removeItem('userName')
		window.dispatchEvent(new Event('authChange'))
		setUser(null)
		setIsOpen(false)
		navigate('/login')
	}

	const handleClickOutside = event => {
		if (menuRef.current && !menuRef.current.contains(event.target)) {
			setIsOpen(false)
		}
	}

	useEffect(() => {
		document.addEventListener('mousedown', handleClickOutside)
		return () => document.removeEventListener('mousedown', handleClickOutside)
	}, [])

	// Обработчик отправки поиска
	const handleSearchSubmit = e => {
		e.preventDefault()
		if (searchQuery.trim()) {
			navigate(`/search?search=${encodeURIComponent(searchQuery.trim())}`)
			setSearchQuery('') // очищаем поле после отправки (можно убрать)
		}
	}

	return (
		<header className={S.header}>
			<div className={S.nav_container}>
				<NavLink to='/' className={S.logo}>
					<span className={S.logo_icon}>🎮</span>
					GameForum
				</NavLink>

				<form className={S.header_search} onSubmit={handleSearchSubmit}>
					<input
						type='text'
						className={S.hero_search_input}
						placeholder='Поиск игр...'
						value={searchQuery}
						onChange={e => setSearchQuery(e.target.value)}
					/>
				</form>

				<div className={S.header_actions}>
					{/* Кнопка ТГ бота */}
					<a
						href='https://t.me/game_news_bot_1_bot'
						target='_blank'
						rel='noreferrer'
						className={S.tg_button}
					>
						<svg
							width='20'
							height='20'
							viewBox='0 0 24 24'
							fill='none'
							className={S.tg_icon_svg}
						>
							<path
								d='M22 2L2 10.5L9 13.5M22 2L15 22L9 13.5M22 2L9 13.5'
								stroke='white'
								strokeWidth='2'
								strokeLinecap='round'
								strokeLinejoin='round'
							/>
							<path
								d='M9 13.5V19L12 16'
								stroke='white'
								strokeWidth='2'
								strokeLinecap='round'
								strokeLinejoin='round'
							/>
						</svg>
						<span className={S.tg_text}>Бот</span>
					</a>

					<div className={S.profile_wrapper} ref={menuRef}>
						{user ? (
							<>
								<div
									className={S.profile_section}
									onClick={() => setIsOpen(!isOpen)}
								>
									<div className={S.profile_icon}>👤</div>
									<div className={S.profile_name}>{user}</div>
								</div>

								{isOpen && (
									<div className={S.popup_menu}>
										<ul className={S.menu_list}>
											<li className={S.menu_item}>
												<NavLink
													to='/profile'
													className={S.navlink}
													onClick={() => setIsOpen(false)}
												>
													Профиль
												</NavLink>
											</li>
											<li className={S.menu_item}>
												<NavLink
													to='#'
													className={S.navlink}
													onClick={() => setIsOpen(false)}
												>
													Избранное
												</NavLink>
											</li>
											<li className={S.menu_item}>
												<NavLink
													to='#'
													className={S.navlink}
													onClick={() => setIsOpen(false)}
												>
													Настройки
												</NavLink>
											</li>
											<div className={S.menu_divider} />
											<li className={S.menu_item}>
												<NavLink
													to='/login'
													className={S.navlink}
													onClick={handleLogout}
												>
													Выйти
												</NavLink>
											</li>
										</ul>
									</div>
								)}
							</>
						) : (
							<NavLink to='/login' className={S.tg_button}>
								<span className={S.tg_text}>Войти</span>
							</NavLink>
						)}
					</div>
				</div>
			</div>
		</header>
	)
}

export default Header
