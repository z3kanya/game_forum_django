import React, { useState, useEffect } from 'react'
import { useSearchParams, Link } from 'react-router-dom'
import Header from './Header'
import Sidebar from './Sidebar'
import SkeletonLoader from './SkeletonLoader'
import styles from '../style/GamesPage.module.css'

// Получаем контекст для папки img (аналогично странице игры)
const imgContext = require.context('../img/', true, /\.(jpg|jpeg|png)$/)
const allPaths = imgContext.keys()

// Функция поиска картинки для игры
const getGameImage = gameName => {
	// Ищем папку, которая точно совпадает с названием игры
	const folderName = gameName
	// Ищем в путях файл, который лежит в папке folderName и содержит "LOGO" или "Заставка"
	const logoPath = allPaths.find(
		path =>
			path.includes(`./${folderName}/`) &&
			(path.includes('LOGO') || path.includes('Заставка')),
	)
	if (logoPath) return imgContext(logoPath)

	// Если не нашли LOGO/Заставку, берём любой файл из папки
	const anyPath = allPaths.find(path => path.includes(`./${folderName}/`))
	if (anyPath) return imgContext(anyPath)

	// Если ничего не нашли, возвращаем null
	return null
}

const GamesPage = () => {
	const [searchParams] = useSearchParams()
	const query = searchParams.get('search') || ''
	const [games, setGames] = useState([])
	const [nextPage, setNextPage] = useState(null)
	const [loading, setLoading] = useState(true)
	const [error, setError] = useState(null)

	const fetchGames = async (url, isLoadMore = false) => {
		try {
			if (!isLoadMore) setLoading(true)
			const response = await fetch(url)
			if (!response.ok) throw new Error('Ошибка загрузки')
			const data = await response.json()
			const results = data.results || data
			setGames(prev => (isLoadMore ? [...prev, ...results] : results))
			setNextPage(data.next)
		} catch (err) {
			setError(err.message)
		} finally {
			if (!isLoadMore) setLoading(false)
		}
	}

	useEffect(() => {
		if (query) {
			setGames([])
			setNextPage(null)
			const url = `http://127.0.0.1:8000/api/games/list/?search=${encodeURIComponent(query)}`
			fetchGames(url, false)
		} else {
			setGames([])
			setLoading(false)
		}
	}, [query])

	const loadMore = () => {
		if (nextPage) fetchGames(nextPage, true)
	}

	return (
		<div className={styles.shader}>
			<Header />
			<div className={styles.mainContainer}>
				<Sidebar />
				<div className={styles.content}>
					{query && (
						<h1 className={styles.title}>
							Результаты поиска: <span className={styles.query}>{query}</span>
						</h1>
					)}
					{error && <div className={styles.error}>{error}</div>}
					{loading && games.length === 0 ? (
						<SkeletonLoader type='list' count={3} />
					) : games.length > 0 ? (
						<>
							<div className={styles.gamesGrid}>
								{games.map(game => {
									const imageUrl = getGameImage(game.name)
									return (
										<Link
											to={`/game/${game.id}`}
											key={game.id}
											className={styles.gameCard}
										>
											{imageUrl ? (
												<img
													src={imageUrl}
													alt={game.name}
													className={styles.gameImage}
												/>
											) : (
												<div className={styles.gameImagePlaceholder}>🎮</div>
											)}
											<div className={styles.gameInfo}>
												<h3>{game.name}</h3>
												<p>{game.description?.slice(0, 80)}...</p>
												{game.genres && (
													<span className={styles.genres}>
														{game.genres.map(g => g.name).join(', ')}
													</span>
												)}
											</div>
										</Link>
									)
								})}
							</div>
							{nextPage && (
								<div className={styles.loadMoreWrapper}>
									<button
										onClick={loadMore}
										disabled={loading}
										className={styles.loadMoreBtn}
									>
										{loading ? 'Загрузка...' : 'Показать больше'}
									</button>
								</div>
							)}
						</>
					) : (
						query && <p className={styles.noResults}>Ничего не найдено.</p>
					)}
				</div>
			</div>
		</div>
	)
}

export default GamesPage
