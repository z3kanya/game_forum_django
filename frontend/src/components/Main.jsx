import React, { useState, useEffect } from 'react'
import S from '../style/Main.module.css'
import Post from './Post'
import Sidebar from './Sidebar'
import Header from './Header'
import SkeletonLoader from './SkeletonLoader'
import { useLocation } from 'react-router-dom'

export default function Main() {
	const [news, setNews] = useState([])
	const [loading, setLoading] = useState(true)
	const [loadingMore, setLoadingMore] = useState(false) // для кнопки "Показать больше"
	const [nextPageUrl, setNextPageUrl] = useState(null) // URL следующей страницы
	const location = useLocation() // хук для отслеживания изменений в URL (сортировки)

	// Универсальная функция загрузки новостей
	const fetchNews = async (url, isLoadMore = false) => {
		try {
			if (!isLoadMore) setLoading(true)
			else setLoadingMore(true)

			// извлекаем параметр ordering из URL (?ordering=-likes_count_attr) – он уже в url, не трогаем
			let token = localStorage.getItem('userToken')
			if (token) {
				token = token.replace(/"/g, '').trim()
			}

			const requestHeaders = {
				'Content-Type': 'application/json',
			}

			if (token) {
				requestHeaders['Authorization'] = `Bearer ${token}`
			}

			const response = await fetch(url, {
				method: 'GET',
				headers: requestHeaders,
			})

			if (!response.ok) throw new Error('Ошибка загрузки')
			const data = await response.json()
			const newsData = data.results || data

			// Добавляем новые новости к старым (если подгружаем) или заменяем
			setNews(prev => (isLoadMore ? [...prev, ...newsData] : newsData))
			setNextPageUrl(data.next) // сохраняем ссылку на следующую страницу

			// искусственная задержка для скелетона (только при первой загрузке)
			if (!isLoadMore) {
				await new Promise(resolve => setTimeout(resolve, 800))
			}
		} catch (error) {
			console.error('Ошибка при загрузке новостей:', error)
		} finally {
			if (!isLoadMore) setLoading(false)
			else setLoadingMore(false)
		}
	}

	// Загружаем первую страницу при монтировании и при изменении сортировки
	useEffect(() => {
		const queryParams = new URLSearchParams(location.search)
		const ordering = queryParams.get('ordering') || '-published_at' // по умолчанию новые
		const initialUrl = `http://127.0.0.1:8000/api/news/news/?ordering=${ordering}`
		fetchNews(initialUrl, false)
	}, [location.search])

	const handleLoadMore = () => {
		if (nextPageUrl) {
			fetchNews(nextPageUrl, true)
		}
	}

	const queryParams = new URLSearchParams(location.search)
	const ordering = queryParams.get('ordering')

	let subTitle = 'новые'

	if (ordering === '-likes_count_attr') {
		subTitle = 'популярные'
	} else if (ordering === '-published_at') {
		subTitle = 'новые'
	}

	return (
		<div>
			<Header />
			<div className={S.main_container}>
				<Sidebar />
				<div className={S.content}>
					<h2 className={S.section_title}>
						Статьи <span className={S.subtitle}>/ {subTitle}</span>
					</h2>
					<div className={S.posts_list}>
						{loading ? (
							<SkeletonLoader type='list' count={3} />
						) : news.length > 0 ? (
							<>
								{news.map(item => (
									<Post key={item.id} data={item} />
								))}
								{nextPageUrl && (
									<div className={S.loadMoreWrapper}>
										<button
											onClick={handleLoadMore}
											disabled={loadingMore}
											className={S.loadMoreBtn}
										>
											{loadingMore ? 'Загрузка...' : 'Показать больше'}
										</button>
									</div>
								)}
							</>
						) : (
							<p>Новостей пока нет...</p>
						)}
					</div>
				</div>
			</div>
		</div>
	)
}
