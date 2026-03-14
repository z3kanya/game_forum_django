import React, { useState, useEffect } from 'react'
import Header from '../components/Header'
import S from '../style/Profile.module.css'
import FavouriteItem from '../components/FavouriteItem'
import Logo from '../img/Atomic Heart/LOGO.jpeg'

const Profile = () => {
	const [isEditing, setIsEditing] = useState(false)
	const [loading, setLoading] = useState(true)
	const [games, setGames] = useState([])

	const [data, setData] = useState({
		username: '',
		name: '',
		email: '',
		telegram: '',
		avatar: '',
	})

	// Состояния для аватарки
	const [avatarFile, setAvatarFile] = useState(null)
	const [avatarPreview, setAvatarPreview] = useState(null)

	// Загрузка профиля
	useEffect(() => {
		const fetchProfile = async () => {
			const token = localStorage.getItem('userToken')?.replace(/"/g, '').trim()

			try {
				const response = await fetch(
					'http://127.0.0.1:8000/api/core/profile/',
					{
						headers: { Authorization: `Bearer ${token}` },
					},
				)

				if (response.ok) {
					const profileData = await response.json()
					setData({
						username: profileData.username,
						name: profileData.first_name || 'Не указано',
						email: profileData.email,
						telegram: profileData.tg_username || '@не_привязан',
						avatar: profileData.avatar,
					})
				}
			} catch (error) {
				console.error('Ошибка загрузки профиля:', error)
			} finally {
				setLoading(false)
			}
		}

		fetchProfile()
	}, [])

	// загрузка логотипов (было)
	const context = require.context('../img/', true, /LOGO\.jpeg$/)
	const imageMap = {}
	context.keys().forEach(path => {
		const folderName = path.split('/')[1]
		imageMap[folderName] = context(path)
	})

	// загрузка избранного
	useEffect(() => {
		const fetchFavorites = async () => {
			const token = localStorage.getItem('userToken')?.replace(/"/g, '').trim()
			try {
				const response = await fetch(
					'http://127.0.0.1:8000/api/games/favorites/',
					{
						headers: { Authorization: `Bearer ${token}` },
					},
				)
				const result = await response.json()
				const finalData = result.results || result
				setGames(finalData)
			} catch (error) {
				console.error('Ошибка загрузки избранного:', error)
			} finally {
				setLoading(false)
			}
		}
		fetchFavorites()
	}, [])

	// удаление из избранного
	const handleRemove = async gameId => {
		const token = localStorage.getItem('userToken')?.replace(/"/g, '').trim()
		const url = `http://127.0.0.1:8000/api/games/${gameId}/favorite/remove/`

		try {
			const response = await fetch(url, {
				method: 'DELETE',
				headers: { Authorization: `Bearer ${token}` },
			})

			if (response.ok) {
				setGames(prev =>
					prev.filter(item => {
						const idInItem = item.game_details?.id || item.game || item.id
						return idInItem !== gameId
					}),
				)
			} else {
				alert('Не удалось удалить из избранного')
			}
		} catch (error) {
			console.error('Ошибка при удалении:', error)
		}
	}

	// выбор файла аватарки
	const handleAvatarChange = e => {
		const file = e.target.files[0]
		if (file) {
			setAvatarFile(file)
			setAvatarPreview(URL.createObjectURL(file))
		}
	}

	// сохранение изменений
	const handleButtonClick = async () => {
		if (isEditing) {
			const token = localStorage.getItem('userToken')?.replace(/"/g, '').trim()

			const formData = new FormData()
			formData.append('first_name', data.name)
			formData.append('email', data.email)
			formData.append('tg_username', data.telegram)
			if (avatarFile) {
				formData.append('avatar', avatarFile)
			}

			try {
				const response = await fetch(
					'http://127.0.0.1:8000/api/core/profile/update/',
					{
						method: 'PATCH',
						headers: { Authorization: `Bearer ${token}` },
						body: formData,
					},
				)

				if (response.ok) {
					const updatedUser = await response.json()
					if (updatedUser.username) {
						localStorage.setItem('userName', updatedUser.username)
					}
					setData(prev => ({
						...prev,
						username: updatedUser.username,
						name: updatedUser.first_name || prev.name,
						email: updatedUser.email,
						telegram: updatedUser.tg_username,
						avatar: updatedUser.avatar,
					}))
					setAvatarFile(null)
					setAvatarPreview(null)
					alert('Данные успешно сохранены!')
					setIsEditing(false)
				} else {
					const errorData = await response.json()
					console.error('Ошибка сервера:', errorData)
					alert(`Ошибка: ${JSON.stringify(errorData)}`)
				}
			} catch (error) {
				console.error('Ошибка сети:', error)
				alert('Не удалось связаться с сервером')
			}
		} else {
			setIsEditing(true)
		}
	}

	// изменение текстовых полей
	const handleChange = (field, value) => {
		setData(prev => ({ ...prev, [field]: value }))
	}

	return (
		<div className={S.wrapper}>
			<Header />
			<div className={S.container}>
				{/* Блок профиля */}
				<div
					className={S.content}
					style={{ marginBottom: '40px', minHeight: 'auto' }}
				>
					<div className={S.container_info}>
						<div className={S.avatar_section}>
							<div className={S.avatar_wrapper}>
								{data.avatar || avatarPreview ? (
									<img
										src={avatarPreview || data.avatar}
										alt='avatar'
										className={S.avatar_img}
									/>
								) : (
									<div className={S.profile_icon}>👤</div>
								)}
							</div>
							{isEditing && (
								<>
									<input
										type='file'
										accept='image/*'
										onChange={handleAvatarChange}
										style={{ marginTop: '10px' }}
									/>
									{avatarPreview && (
										<button
											onClick={() => {
												setAvatarFile(null)
												setAvatarPreview(null)
											}}
											style={{ marginLeft: '10px' }}
										>
											Отменить
										</button>
									)}
								</>
							)}
						</div>

						<div className={S.data_section}>
							<div className={S.column_left}>
								<div className={S.data_item}>
									{isEditing ? (
										<>
											<label>Ник:</label>
											<input
												type='text'
												value={data.username}
												disabled
												className={S.input}
											/>
										</>
									) : (
										<h4>Ник: {data.username}</h4>
									)}
								</div>
								<div className={S.data_item}>
									{isEditing ? (
										<>
											<label>Имя:</label>
											<input
												type='text'
												value={data.name}
												onChange={e => handleChange('name', e.target.value)}
												className={S.input}
											/>
										</>
									) : (
										<h4>Имя: {data.name}</h4>
									)}
								</div>
							</div>

							<div className={S.column_right}>
								<div className={S.data_item}>
									{isEditing ? (
										<>
											<label>Почта:</label>
											<input
												type='email'
												value={data.email}
												onChange={e => handleChange('email', e.target.value)}
												className={S.input}
											/>
										</>
									) : (
										<h4>Почта: {data.email}</h4>
									)}
								</div>
								<div className={S.data_item}>
									{isEditing ? (
										<>
											<label>Telegram:</label>
											<input
												type='text'
												value={data.telegram}
												onChange={e => handleChange('telegram', e.target.value)}
												className={S.input}
											/>
										</>
									) : (
										<h4>Telegram: {data.telegram}</h4>
									)}
								</div>
								<button className={S.btn_edit} onClick={handleButtonClick}>
									{isEditing ? 'Сохранить' : 'Изменить данные'}
								</button>
							</div>
						</div>
					</div>
				</div>

				{/* Блок избранного */}
				<div className={S.content}>
					<h2 className={S.heading}>Избранное</h2>
					<div className={S.favorite_list}>
						{loading ? (
							<div style={{ color: '#fff' }}>Загрузка списка...</div>
						) : games.length > 0 ? (
							games.map(item => {
								const gameData = item.game_details || item
								return (
									<FavouriteItem
										key={item.id}
										game={gameData}
										logo={imageMap[gameData.name] || Logo}
										onRemove={() => handleRemove(gameData.id)}
									/>
								)
							})
						) : (
							<div style={{ color: '#ccc', padding: '20px' }}>
								Список избранного пуст
							</div>
						)}
					</div>
				</div>
			</div>
		</div>
	)
}

export default Profile
